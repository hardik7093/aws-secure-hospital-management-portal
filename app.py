from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import pymysql
import boto3
import json
import logging

app = Flask(__name__)

# ======================================
# AWS Configuration
# ======================================

REGION = "us-east-1"
SECRET_NAME = "hospital-db-secret"
BUCKET_NAME = "hardik-hospital-reports-2026"

# ======================================
# Logging Configuration
# ======================================

logging.basicConfig(
    filename="hospital.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ======================================
# Get Database Secret
# ======================================

def get_db_secret():
    client = boto3.client(
        "secretsmanager",
        region_name=REGION
    )

    response = client.get_secret_value(
        SecretId=SECRET_NAME
    )

    return json.loads(response["SecretString"])

secret = get_db_secret()

# ======================================
# Database Connection
# ======================================

connection = pymysql.connect(
    host=secret["host"],
    user=secret["username"],
    password=secret["password"],
    database=secret["database"],
    port=int(secret["port"]),
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)

# ======================================
# AWS Clients
# ======================================

s3 = boto3.client(
    "s3",
    region_name=REGION
)

sns = boto3.client(
    "sns",
    region_name=REGION
)

TOPIC_ARN = "arn:aws:sns:us-east-1:515966516119:hospital-notification-topic"

# ======================================
# Dashboard
# ======================================

@app.route("/")
def home():

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM patients
        ORDER BY id DESC
    """)

    patients = cursor.fetchall()

    logging.info("Dashboard accessed.")

    return render_template(
        "dashboard.html",
        patients=patients
    )

# ======================================
# Add Patient
# ======================================

@app.route("/add", methods=["POST"])
def add_patient():

    try:

        name = request.form["name"]
        age = request.form["age"]
        disease = request.form["disease"]
        doctor = request.form["doctor"]

        report = request.files["report"]

        filename = ""

        # Upload report to S3
        if report and report.filename != "":

            filename = secure_filename(report.filename)

            s3.upload_fileobj(
                report,
                BUCKET_NAME,
                filename
            )

            logging.info(f"Report uploaded to S3 : {filename}")

        # Save to RDS
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO patients
            (name, age, disease, doctor, report_file)

            VALUES
            (%s,%s,%s,%s,%s)
            """,
            (
                name,
                age,
                disease,
                doctor,
                filename
            )
        )

        logging.info(f"Patient Added : {name}")

        # SNS Notification
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="New Patient Registered",
            Message=f"""
🏥 AWS Secure Hospital Management Portal

A new patient has been registered successfully.

----------------------------------------

Patient Name : {name}
Age          : {age}
Disease      : {disease}
Doctor       : {doctor}

Medical Report : {filename}

----------------------------------------

Services Used

✅ Amazon EC2
✅ Amazon RDS
✅ Amazon S3
✅ AWS Secrets Manager
✅ Amazon SNS

This notification was generated automatically.
"""
        )

        logging.info(f"SNS Notification Sent for {name}")

        return redirect("/")

    except Exception as e:

        logging.error(f"Application Error : {str(e)}")

        return f"Error : {e}"

# ======================================
# Run Flask
# ======================================

if __name__ == "__main__":

    logging.info("Hospital Management Portal Started")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
