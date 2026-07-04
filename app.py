from flask import Flask, render_template, request, redirect
import pymysql
import boto3
import json

app = Flask(__name__)

# Get database credentials from AWS Secrets Manager
def get_db_secret():
    client = boto3.client(
        "secretsmanager",
        region_name="us-east-1"
    )

    response = client.get_secret_value(
        SecretId="hospital-db-secret"
    )

    return json.loads(response["SecretString"])

# Load secret
secret = get_db_secret()

# Create MySQL connection
connection = pymysql.connect(
    host=secret["host"],
    user=secret["username"],
    password=secret["password"],
    database=secret["database"],
    port=int(secret["port"]),
    cursorclass=pymysql.cursors.DictCursor
)

@app.route("/")
def home():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY id DESC")
    patients = cursor.fetchall()
    return render_template("dashboard.html", patients=patients)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    age = request.form["age"]
    disease = request.form["disease"]
    doctor = request.form["doctor"]

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO patients(name, age, disease, doctor) VALUES (%s, %s, %s, %s)",
        (name, age, disease, doctor)
    )

    connection.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
