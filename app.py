import streamlit as st
import time
import re
from dotenv import load_dotenv

from aws_utils import (
    detect_license_plate,
    describe_image_violations,
    classify_violation,
    lookup_owner_info,
    store_violation_record
)

from auth import register_user, confirm_user, login_user
from redshift_utils import insert_violation
from email_utils import send_violation_email

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(page_title="Traffic Violation Reporter", layout="wide")

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "useremail" not in st.session_state:
    st.session_state["useremail"] = ""


# 🔐 Login Tab
def login_tab():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        success, result = login_user(email, password)
        if success and isinstance(result, dict):
            st.session_state["authenticated"] = True
            st.session_state["username"] = result.get("username", "User")
            st.session_state["useremail"] = result.get("email", email)
            st.success(f"✅ Welcome, {st.session_state['username']}")
            st.rerun()
        else:
            st.error(f"❌ Login failed: {result}")

# 📝 Registration Tab
def register_tab():
    st.subheader("Register")

    username = st.text_input("Full Name / Username", key="reg_username")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")
    st.markdown(
        "<span style='font-size: 12px; color: gray;'>Password must be at least 8 characters, include a capital letter, number, and symbol.</span>",
        unsafe_allow_html=True
    )

    if st.button("Get Code"):
        if not email or not password or not username:
            st.warning("Please fill in all fields.")
        else:
            success, msg = register_user(email, password, username)
            if success:
                st.success(msg)
            else:
                if "UsernameExistsException" in msg:
                    st.error("❌ This email is already registered. Please log in instead.")
                else:
                    st.error(f"❌ Registration failed: {msg}")

    code = st.text_input("Verification Code (Check your Email)", key="reg_code")

    if st.button("Verify"):
        success, msg = confirm_user(email, code)
        if success:
            st.success(msg)
            st.session_state["switch_to_login"] = True
            st.session_state["just_verified"] = True
            time.sleep(2)
            st.rerun()
        else:
            st.error(msg)

# 🚧 Show login or registration if not authenticated
if not st.session_state["authenticated"]:
    st.title("🚨 Traffic Violation Reporter")
    tabs = st.tabs(["Login", "Register"])
    with tabs[0]:
        login_tab()
    with tabs[1]:
        register_tab()
    st.stop()


# ✅ Main App After Login
st.title("🚦 Report a Traffic Violation")

uploaded_file = st.file_uploader("Upload a traffic violation image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", width=400)

    if st.button("Report"):
        license_plate = detect_license_plate(uploaded_file)
        st.write("🔍 **Detected License Plate:**", license_plate)

        description = describe_image_violations(uploaded_file)
        st.write("📝 **Description Generated:**", description)

        violation_type = classify_violation(description)
        st.write("🚫 **Violation Type:**", violation_type)

        store_violation_record(
            license_plate=license_plate,
            violation_type=violation_type,
            description=description,
            username=st.session_state.get("username", "unknown_user"),
            email=st.session_state.get("useremail", "unknown_email")
        )

        st.success("✅ Violation record saved in DynamoDB!")

        owner_info = lookup_owner_info(license_plate)
        if owner_info:
            phone = str(owner_info.get("contact_number", "Not Found"))
            email = owner_info.get("email", "Not Found")
            st.info(f"📇 **Owner Details:**\n- Phone: {phone}\n- Email: {email}")

            # 📤 Send notification email
            if send_violation_email(email, license_plate, violation_type, description):
                st.success("📧 Email notification sent to the vehicle owner.")
            else:
                st.warning("⚠️ Failed to send email notification.")
        else:
            st.warning("⚠️ No owner info found for this license plate.")
