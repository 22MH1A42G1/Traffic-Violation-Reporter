📄 Traffic Violation Reporter – Full Setup Guide for GitHub

This document will help you set up all the AWS services and local environment needed to successfully run the Traffic Violation Reporter project from your GitHub repository.


---

✅ Step 1: Clone the GitHub Repository

git clone https://github.com/22MH1A42G1/traffic-violation-reporter-with-vehicle-number-detection.git
cd traffic-violation-reporter-with-vehicle-number-detection


---

🔐 Step 2: Set Up AWS Cognito (User Authentication)

✅ Create User Pool

1. Open AWS Console → Search for Cognito → Click Create user pool


2. Choose "Federated Identities" → "User Pools" → Create user pool


3. Name: TrafficViolationUserPool


4. Attributes:

Select email as the required attribute

Allow self sign-up with email



5. Security settings:

Set password policy (default is okay)



6. MFA and verifications:

Enable email verification



7. App Client:

Click "Add app client"

Disable client secret



8. Save your:

User Pool ID

App Client ID




🧠 AWS CLI Commands

aws cognito-idp list-user-pools --max-results 10


---

📸 Step 3: Set Up AWS Rekognition (For License Plate Detection)

No manual configuration needed. Just ensure Rekognition is enabled in your region.

🧠 Required IAM Permissions

{
  "Effect": "Allow",
  "Action": ["rekognition:DetectText"],
  "Resource": "*"
}

🧠 AWS CLI Test Command

aws rekognition detect-text \
--image "S3Object={Bucket=my-bucket,Name=my-image.jpg}" \
--region us-east-1


---

🤖 Step 4: Set Up AWS Bedrock (LLM for Violation Description)

✅ Enable Bedrock Access

1. Open Amazon Bedrock Console


2. Go to Model Access → Enable Meta (LLaMA 3)



🧠 Required IAM Policy

{
  "Effect": "Allow",
  "Action": ["bedrock:*"],
  "Resource": "*"
}

Bedrock doesn’t require any resource creation — access and permissions are enough.

🧠 AWS CLI Model List

aws bedrock list-foundation-models


---

💾 Step 5: Set Up AWS DynamoDB

✅ Create Table: ViolationRecords

aws dynamodb create-table \
--table-name ViolationRecords \
--attribute-definitions AttributeName=violation_id,AttributeType=S \
--key-schema AttributeName=violation_id,KeyType=HASH \
--billing-mode PAY_PER_REQUEST

Add data manually or via code.

✅ Create Table: VehicleOwners

aws dynamodb create-table \
--table-name VehicleOwners \
--attribute-definitions AttributeName=license_plate,AttributeType=S \
--key-schema AttributeName=license_plate,KeyType=HASH \
--billing-mode PAY_PER_REQUEST

🧠 Sample Insert via CLI

aws dynamodb put-item \
--table-name VehicleOwners \
--item '{"license_plate": {"S": "MH12AB1234"}, "contact_number": {"S": "9876543210"}, "email": {"S": "owner@example.com"}}'


---

🔑 Step 6: Create IAM User with Required Permissions

🧠 AWS CLI

aws iam create-user --user-name traffic-admin

Attach this policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {"Effect": "Allow", "Action": "rekognition:*", "Resource": "*"},
    {"Effect": "Allow", "Action": "bedrock:*", "Resource": "*"},
    {"Effect": "Allow", "Action": "dynamodb:*", "Resource": "*"},
    {"Effect": "Allow", "Action": "cognito-idp:*", "Resource": "*"}
  ]
}

Generate Access Key ID and Secret Access Key.


---

⚙️ Step 7: Configure Environment Variables

Create a .env file in your project root with:

AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

COGNITO_CLIENT_ID=your_client_id
COGNITO_POOL_ID=your_pool_id

GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_app_password


---

🖥️ Step 8: Run the App Locally

🧠 Commands

pip install -r requirements.txt
python -m streamlit run app.py

Access it at: http://localhost:8501


---

☁️ Step 9: Deploy on EC2 (Ubuntu)

🧠 SSH & Setup

ssh -i your-key.pem ubuntu@your-ec2-ip

sudo apt update
sudo apt install python3-pip git -y

git clone https://github.com/22MH1A42G1/traffic-violation-reporter-with-vehicle-number-detection.git
cd traffic-violation-reporter-with-vehicle-number-detection

pip3 install -r requirements.txt

Add your .env file

🧠 Start App

streamlit run app.py --server.port 8501 --server.enableCORS false

To keep it running in background:

nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &

Visit: http://<your-ec2-ip>:8501


---

📌 Checklist Summary

[x] GitHub repo cloned

[x] Cognito pool and client created

[x] Rekognition ready

[x] Bedrock model access granted

[x] DynamoDB tables created

[x] IAM user created

[x] Environment variables set

[x] Streamlit app deployed locally or on EC2



---

👨‍💻 Maintained by

Indana Aditya
GitHub • LinkedIn



✅ Your Document.md file has been updated with detailed setup instructions, including:

✅ How to create Cognito User Pools (with CLI commands)

✅ How to configure Amazon Rekognition

✅ Steps to enable Bedrock

✅ How to create and set up DynamoDB tables

✅ IAM Role creation and permissions

✅ Example AWS CLI commands for each task


Would you also like:

A .sh setup script to automate these commands?

Screenshots or diagrams added to the documentation? Let me know how you'd like to enhance it further!


