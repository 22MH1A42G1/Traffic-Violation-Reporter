from pycognito import Cognito

# Replace with your actual values
USER_POOL_ID = "us-east-1_rrGVWzW84"
CLIENT_ID = "4bs4p80kt78kqrf4esklsdigjk"
REGION = "us-east-1"

def register_user(email, password, username):
    try:
        user = Cognito(USER_POOL_ID, CLIENT_ID, user_pool_region=REGION)
        # Set 'name' attribute so it can be retrieved later
        user.set_base_attributes(email=email, name=username)
        user.register(username=email, password=password)
        return True, "Registered successfully. Check your email for the confirmation code."
    except Exception as e:
        return False, f"❌ Registration failed: {repr(e)}"

def confirm_user(email, code):
    try:
        user = Cognito(USER_POOL_ID, CLIENT_ID, username=email, user_pool_region=REGION)
        user.confirm_sign_up(code)
        return True, "✅ User confirmed successfully."
    except Exception as e:
        if "Current status is CONFIRMED" in str(e):
            return True,("✅ User is already confirmed. Please log in.")
        return False, f"❌ Confirmation failed: {repr(e)}"

def login_user(email, password):
    try:
        user = Cognito(USER_POOL_ID, CLIENT_ID, username=email, user_pool_region=REGION)
        user.authenticate(password)

        try:
            user.get_user()  # Fetch user attributes
            attributes = user.user_attributes

            # Default to email as fallback
            username = email

            # Try to get the name or custom:username attribute
            for attr in attributes:
                if attr["Name"] in ["name", "custom:username"]:
                    username = attr["Value"]
                    break

        except Exception as attr_error:
            username = email  # fallback
            print("⚠ Warning: Failed to get attributes:", repr(attr_error))

        return True, {
            "username": username,
            "email": email
        }

    except Exception as e:
        return False, f"❌ Login failed: {repr(e)}"