import boto3
import os
import json
import uuid
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# AWS clients
rekognition = boto3.client("rekognition", region_name=AWS_REGION)
bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

# 1️⃣ Detect license plate using Rekognition
def detect_license_plate(image_file):
    img_bytes = image_file.read()
    response = rekognition.detect_text(Image={'Bytes': img_bytes})
    image_file.seek(0)

    for text in response['TextDetections']:
        detected = text['DetectedText']
        if text['Type'] == 'LINE' and any(char.isdigit() for char in detected) and len(detected) >= 6:
            return detected
    return "UNKNOWN"

# 2️⃣ Generate description of the violation
def describe_image_violations(image_file):
    image_file.seek(0)
    image_bytes = image_file.read()
    image_file.seek(0)

    # Extract detailed image properties from Rekognition
    rek_response = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=20,
        Features=["GENERAL_LABELS"],
        MinConfidence=70
    )

    # Build a structured JSON of detected objects
    structured_labels = []
    for label in rek_response['Labels']:
        label_info = {
            "Label": label['Name'],
            "Confidence": round(label['Confidence'], 2),
            "Instances": len(label.get("Instances", [])),
            "Parents": [p["Name"] for p in label.get("Parents", [])]
        }
        structured_labels.append(label_info)

    image_summary = {
        "detected_objects": structured_labels
    }

    # 🧠 Pass the full structured JSON to LLM
    prompt = f"""
You are an AI system trained to analyze traffic images for violations.

Here is the detailed information detected in the image:
{json.dumps(image_summary, indent=2)}

Based on this data, determine if any traffic violations are clearly visible. Focus on:
- Helmetless riding
- Triple riding
- Overloading
- Minor riding
- Mobile usage while riding
- Signal jumping

Return a **clean comma-separated list** of only the violations. If no violations are seen, return:
`No violations detected`
"""

    body = {
        "prompt": prompt,
        "max_gen_len": 300,
        "temperature": 0.3,
        "top_p": 0.9
    }

    response = bedrock.invoke_model(
        modelId="meta.llama3-70b-instruct-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read().decode())
    return result.get("generation", "").strip()

# 3️⃣ Classify violation
import re

def classify_violation(description):
    prompt = f"""
You are a strict traffic rule classification AI.

From the following description:
\"{description}\"

Extract and return only the violation label(s), such as:
- Helmetless riding
- Triple riding
- Signal breaking
- Mobile usage while driving

If multiple violations are mentioned, return a comma-separated list.

Do NOT include any explanation or extra text.
Only return the labels.
"""

    body = {
        "prompt": prompt,
        "max_gen_len": 50,
        "temperature": 0.2,
        "top_p": 0.9
    }

    response = bedrock.invoke_model(
        modelId="meta.llama3-70b-instruct-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read().decode())
    raw_output = result.get("generation", "").strip()

    # 🔍 Optional regex fallback if model output is messy
    matches = re.findall(r'(Helmetless riding|Triple riding|Signal breaking|Mobile usage(?: while driving)?)', raw_output, re.IGNORECASE)
    return ", ".join(set(m.title() for m in matches)) if matches else "Unknown Violation"


# 4️⃣ Store violation to DynamoDB with IST timestamp
def store_violation_record(license_plate, violation_type, description, username, email=None):
    table = dynamodb.Table('ViolationRecords')

    # Format IST time
    ist = pytz.timezone('Asia/Kolkata')
    timestamp_ist = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

    item = {
        "violation_id": str(uuid.uuid4()),
        "license_plate": license_plate,
        "Description": violation_type,
        "violation_Type": description,
        "username": username if username else "unknown_user",
        "timestamp": timestamp_ist
    }

    if email:
        item["email"] = email

    table.put_item(Item=item)
    print(f"✅ Violation stored for: {license_plate} by {username}")

# 5️⃣ Lookup vehicle owner details
def lookup_owner_info(license_plate):
    table = dynamodb.Table('VehicleOwners')
    response = table.get_item(Key={'license_plate': license_plate})
    return response.get('Item')
