# 🚦 Traffic Violation Reporter

A web-based AI system that detects and reports traffic violations from uploaded images using AWS services like Rekognition, Bedrock, Cognito, EC2 and DynamoDB. Built with Python and Streamlit, this application supports user authentication, license plate detection, AI-based violation classification, and owner email notifications. Fully deployable on Amazon EC2.

---
## 🏗️ Architecture Overview &  📹 Final Output  

#### Architecture Diagram

[![Architecture](https://github.com/22MH1A42G1/traffic-violation-reporter-with-vehicle-number-detection/blob/main/img/WorkFlow.png)](https://www.youtube.com/watch?v=RBIyEDNF6ic)

---

## 📌 Features

- 🔐 User Authentication via AWS Cognito
- 📸 License Plate Detection with AWS Rekognition
- 🧠 Violation Classification using AWS Bedrock (LLaMA 3)
- 💾 Record Storage in AWS DynamoDB
- 📧 Email Alerts to Vehicle Owners via Gmail SMTP
- 🌐 Clean, responsive frontend using Streamlit
- ☁️ Fully deployable on Amazon EC2

---

## 🧠 Technologies Used

| Component       | Technology            |
|----------------|------------------------|
| Frontend       | Streamlit              |
| Authentication | AWS Cognito            |
| Image Analysis | AWS Rekognition        |
| AI Reasoning   | AWS Bedrock (LLaMA 3)  |
| Database       | AWS DynamoDB           |
| Email Alerts   | Gmail SMTP             |
| Hosting        | Amazon EC2             |
| Language       | Python 3.12            |

---

## 📂 Project Structure

```

traffic-violation-reporter/
│
├── app.py             # Main Streamlit app
├── auth.py            # Cognito login/registration logic
├── aws\_utils.py       # Rekognition, Bedrock, DynamoDB handlers
├── email\_utils.py     # SMTP email alert handler
├── .env               # Environment variables
├── requirements.txt   # Python dependencies
└── README.md          # Documentation

````

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

- AWS account with:
  - Rekognition enabled
  - Bedrock access (LLaMA 3)
  - Cognito User Pool & App Client
  - DynamoDB tables:
    - `ViolationRecords`
    - `VehicleOwners`
- Gmail account with App Password enabled
- Python 3.12+
- EC2 Ubuntu server for deployment

---

### 🗝 Environment Variables

Create a `.env` file with the following:

```env
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

COGNITO_CLIENT_ID=your_cognito_app_client_id
COGNITO_POOL_ID=your_cognito_user_pool_id

GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_gmail_app_password
````

---

### 🧪 DynamoDB Tables

#### 📄 `ViolationRecords`

| Field           | Description                       |
| --------------- | --------------------------------- |
| violation\_id   | Unique UUID                       |
| license\_plate  | Detected plate number             |
| Description     | Clean description (LLM)           |
| violation\_Type | Violation type (helmetless, etc.) |
| username        | Reporter name/email               |
| timestamp       | IST timestamp                     |
| email           | Reporter email (optional)         |

#### 📄 `VehicleOwners`

| Field           | Description           |
| --------------- | --------------------- |
| license\_plate  | Primary key           |
| contact\_number | Owner’s phone number  |
| email           | Owner’s email address |

---

## 🚀 Running Locally

```bash
# Clone repo
git clone https://github.com/22MH1A42G1/traffic-violation-reporter-with-vehicle-number-detection.git
cd traffic-violation-reporter

# Install dependencies
pip install -r requirements.txt

# Start Streamlit app
streamlit run app.py
```

---

## ☁️ EC2 Deployment (Ubuntu)

1. **Launch an EC2 instance** (Ubuntu, t2.micro or higher)
2. SSH into your instance:

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

3. **Install Python & Pip**

```bash
sudo apt update
sudo apt install python3-pip -y
```

4. **Install Git & Clone Repo**

```bash
sudo apt install git -y
git clone https://github.com/22MH1A42G1/traffic-violation-reporter-with-vechicle-number-detection.git
cd traffic-violation-reporter-with-vechicle-number-detection
```

5. **Install requirements**

```bash
pip3 install -r requirements.txt
```

6. **Create `.env` file** with the same values as local

7. **Start the App**

```bash
streamlit run app.py --server.port 8501 --server.enableCORS false
```
> 🔄 Optional: Keep App Running in Background
Use nohup to keep it running after disconnect:

```bash
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

View logs:

```bash
cat nohup.out
```

8. **Open in browser**

* Go to `http://<your-ec2-public-ip>:8501` in your browser

---

## 🧠 How It Works

1. User logs in or registers via AWS Cognito
2. Uploads a traffic image (e.g. bike without helmet)
3. Rekognition extracts license plate
4. Bedrock LLM analyzes image → generates description
5. Description is classified into violations (helmetless, triple riding, etc.)
6. Record stored in DynamoDB
7. Owner details are looked up from `VehicleOwners`
8. If email found, notification is sent via Gmail SMTP

---

## 📧 Email Format

```
Subject: Traffic Violation Notice for MH12AB1234

Dear Vehicle Owner,

Your vehicle with license plate MH12AB1234 was detected violating traffic rules.

Violation Type: Helmetless riding
Details: Helmetless riding, Triple riding

This is an automated notice. Please ensure compliance with road safety regulations.

Regards,
Traffic Authority AI System
```

---

## 📌 Improvements (To-Do)
* [ ] Video-based violation detection support
* [ ] Admin panel to manage violations
* [ ] Violation statistics dashboard
* [ ] Owner verification portal

---
## 🔍 Screenshots

### ☁️ EC2 Deployment
![EC2 Deployment](https://github.com/22MH1A42G1/traffic-violation-reporter-with-vehicle-number-detection/blob/main/img/ec2_deployment_success.png)

### 🚀 Login & Dashboard
![Login Page](https://github.com/22MH1A42G1/traffic-violation-reporter-with-vehicle-number-detection/blob/main/img/login_page.png)
![Streamlit Dashboard](https://github.com/22MH1A42G1/traffic-violation-reporter-with-vehicle-number-detection/blob/main/img/upload_page.png)

### 📷 Violation Detection
![Violation Detection](https://github.com/22MH1A42G1/traffic-violation-reporter-with-vehicle-number-detection/blob/main/img/violation_detection_result.png)

### 📊 DynamoDB Storage
![DynamoDB Entry](https://github.com/22MH1A42G1/traffic-violation-reporter-with-vehicle-number-detection/blob/main/img/dynamoDB_strorage.png)

### 📩 Notification (Gmail)
![Notification](https://github.com/22MH1A42G1/traffic-violation-reporter-with-vehicle-number-detection/blob/main/img/notification.png)


---

## 🧑‍💻 Author

**Indana Aditya**
[LinkedIn](https://www.linkedin.com/in/aditya-indana-899734216) • [GitHub](https://github.com/22MH1A42G1)
