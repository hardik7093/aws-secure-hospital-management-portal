from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

connection = pymysql.connect(
    host="hospital-db.cqz42w2yo835.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Hardik9998",
    database="hospitaldb",
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
        "INSERT INTO patients(name,age,disease,doctor) VALUES(%s,%s,%s,%s)",
        (name, age, disease, doctor)
    )

    connection.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
