# AWS Secure Hospital Management Portal

A cloud-hosted hospital patient management portal built with Flask and integrated with multiple AWS services for secure storage, database access, notifications, event-driven workflows, monitoring, audit logging, and CDN delivery.

## Project Overview

This project demonstrates a secure AWS-based web application where hospital staff can register patients, upload medical reports, store patient records, and trigger automated notifications and events.

The application is deployed on Amazon EC2 and uses Amazon RDS for patient records, Amazon S3 for report storage, AWS Secrets Manager for database credentials, Amazon SNS/SQS/Lambda for asynchronous processing, Amazon EventBridge for event routing, CloudWatch for logging, CloudTrail for audit tracking, and CloudFront for public HTTPS access using the default CloudFront domain.

## Architecture

```text
User
  |
  v
Amazon CloudFront
  |
  v
Amazon EC2 - Flask Application
  |
  |-- AWS Secrets Manager -> Database credentials
  |-- Amazon RDS -> Patient records
  |-- Amazon S3 -> Medical report uploads
  |-- Amazon SNS -> Patient registration notifications
  |-- Amazon EventBridge -> PatientCreated custom events
  |-- Amazon CloudWatch -> Application and service logs
  |-- AWS CloudTrail -> AWS API audit logs
```

## AWS Services Used

| AWS Service | Purpose | Status |
| --- | --- | --- |
| IAM | EC2 role and service permissions | Done |
| VPC | Network isolation and routing | Done |
| EC2 | Hosts the Flask web application | Done |
| RDS | Stores patient records | Done |
| S3 | Stores uploaded medical reports | Done |
| Secrets Manager | Stores database credentials securely | Done |
| SNS | Sends patient registration notifications | Done |
| SQS | Supports asynchronous message processing | Done |
| Lambda | Processes queue-driven or event-driven workflows | Done |
| CloudWatch | Stores logs and monitoring data | Done |
| EventBridge | Publishes `PatientCreated` custom events | Done |
| CloudTrail | Tracks AWS API activity for auditing | Done |
| CloudFront | Provides HTTPS access through CloudFront default domain | Done |
| ALB | Optional future scalability enhancement | Optional |
| Auto Scaling | Optional future scalability enhancement | Optional |
| AWS Backup | Optional production disaster recovery enhancement | Optional |
| WAF | Optional protection layer for ALB/CloudFront | Optional |
| Route 53 + ACM | Optional custom domain and TLS certificate setup | Optional |

## Features

- Patient registration through a Flask dashboard
- Medical report upload to Amazon S3
- Patient data persistence in Amazon RDS
- Secure database credential retrieval from AWS Secrets Manager
- SNS notification after successful patient registration
- EventBridge custom event publishing after patient creation
- CloudWatch log generation for operational visibility
- CloudTrail trail for AWS API audit logging
- CloudFront distribution for public HTTPS access

## Application Flow

1. User opens the hospital portal through CloudFront or the EC2 public endpoint.
2. User submits patient details and uploads a medical report.
3. Flask uploads the report file to Amazon S3.
4. Flask inserts patient metadata into Amazon RDS.
5. Flask publishes a `PatientCreated` event to Amazon EventBridge.
6. Flask sends a notification through Amazon SNS.
7. Logs are written locally and monitored through AWS logging services.
8. CloudTrail records AWS API activity for audit purposes.

## EventBridge Event

The application publishes a custom EventBridge event after a patient is successfully registered.

```json
{
  "Source": "hospital.portal",
  "DetailType": "PatientCreated",
  "EventBusName": "hospital-event-bus",
  "Detail": {
    "patient_name": "Example Patient",
    "age": "30",
    "disease": "Fever",
    "doctor": "Dr Example",
    "report_file": "report.pdf"
  }
}
```

## Tech Stack

- Python
- Flask
- PyMySQL
- Boto3
- HTML/CSS
- Amazon EC2
- Amazon RDS
- Amazon S3
- AWS Secrets Manager
- Amazon SNS
- Amazon SQS
- AWS Lambda
- Amazon EventBridge
- Amazon CloudWatch
- AWS CloudTrail
- Amazon CloudFront

## Local Setup

Clone the repository:

```bash
git clone https://github.com/hardik7093/aws-secure-hospital-management-portal.git
cd aws-secure-hospital-management-portal
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 app.py
```

The application runs on:

```text
http://localhost:5000
```

## EC2 Deployment

On the EC2 instance:

```bash
cd ~/hospital-portal
source venv/bin/activate
nohup python3 app.py > app.out 2>&1 &
```

Verify the app:

```bash
curl -I http://127.0.0.1:5000/
```

Expected response:

```text
HTTP/1.1 200 OK
```

## CloudFront Deployment

CloudFront is configured with the EC2 public DNS as a custom origin.

Recommended origin settings:

```text
Origin domain: EC2 public DNS
Origin protocol: HTTP only
HTTP port: 5000
Viewer protocol policy: Redirect HTTP to HTTPS
Cache policy: CachingDisabled
Origin request policy: AllViewerExceptHostHeader
```

The application can be accessed through the default CloudFront URL:

```text
https://<cloudfront-distribution-domain>.cloudfront.net
```

## Verification Checklist

Use this checklist to validate the complete project:

| Test | Expected Result |
| --- | --- |
| Open app through CloudFront | Dashboard loads successfully |
| Add a patient | Patient appears in dashboard |
| Upload report | File appears in S3 bucket |
| Check RDS table | Patient record is inserted |
| Check `hospital.log` | S3, RDS, SNS, and EventBridge log lines appear |
| Check SNS | Notification is delivered |
| Check EventBridge target logs | `PatientCreated` event appears |
| Check CloudTrail Event history | AWS API activity appears |

Example log lines:

```text
Report uploaded to S3
Patient Added
EventBridge Event Published for Patient
SNS Notification Sent
```

## Security Notes

- Database credentials are not hardcoded in the application.
- Credentials are retrieved securely from AWS Secrets Manager.
- IAM roles are used for EC2-to-AWS service access.
- CloudTrail is enabled for AWS API audit logging.
- CloudFront provides HTTPS access using the default CloudFront certificate.
- For production, restrict EC2 security group access and place the application behind an ALB or private origin.

## Optional Future Enhancements

- Add Application Load Balancer for production-grade traffic routing.
- Add Auto Scaling Group for high availability and horizontal scaling.
- Add AWS Backup for automated RDS backup and recovery.
- Add AWS WAF for managed web protection rules.
- Add Route 53 and ACM for custom domain HTTPS access.
- Add CI/CD deployment using GitHub Actions.

## Cleanup Notes

If this is a temporary AWS demo project, delete unused resources after testing to avoid charges:

- CloudFront distribution
- EC2 instance
- RDS database
- S3 buckets
- CloudTrail S3 log bucket
- EventBridge rules and event bus
- SNS topics and SQS queues
- Lambda functions
- Unused AMIs, snapshots, launch templates, and security groups

## Project Status

| AWS Service | Status |
| --- | --- |
| IAM | Done |
| VPC | Done |
| EC2 | Done |
| RDS | Done |
| S3 | Done |
| Secrets Manager | Done |
| SNS | Done |
| SQS | Done |
| Lambda | Done |
| CloudWatch | Done |
| EventBridge | Done |
| CloudTrail | Done |
| CloudFront | Done |
| ALB | Optional |
| Auto Scaling | Optional |
| AWS Backup | Optional |
| WAF | Optional |
| Route 53 + ACM | Optional |

