from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
from datetime import datetime, timezone

app = Flask(__name__)
POSTGRESQL_URL = "postgres://qbagbicw:fireosUQdGm-xyaJY3xJvTigVuSnl_IE@topsy.db.elephantsql.com/qbagbicw"


connection = psycopg2.connect(POSTGRESQL_URL)
with connection:
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS employees (id SERIAL PRIMARY KEY, emp_id TEXT, password TEXT, name TEXT, salary REAL);")

CREATE_EMPLOYEES_TABLE = "CREATE TABLE IF NOT EXISTS employees (id SERIAL PRIMARY KEY, emp_id TEXT, password TEXT, name TEXT, salary REAL);"

INSERT_EMPLOYEE = "INSERT INTO employees (emp_id, password, name, salary) VALUES (%s, %s, %s, %s);"

GET_EMPLOYEE_SALARY = "SELECT salary, name, emp_id FROM employees WHERE emp_id = %s AND password = %s;"



CREATE_COURSES_TABLE = "CREATE TABLE IF NOT EXISTS courses (id SERIAL PRIMARY KEY, student_id TEXT, course_name TEXT, student_name TEXT, semester TEXT);"
INSERT_COURSE = "INSERT INTO courses (student_id, course_name, student_name, semester) VALUES (%s, %s, %s, %s) RETURNING id;"




connection = psycopg2.connect(POSTGRESQL_URL)
with connection:
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS parking (id SERIAL PRIMARY KEY, name TEXT, student_id TEXT, date DATE, time TIME);")

@app.route("/parking", methods=["GET", "POST"])
def parking_home():
    if request.method == "POST":
        name = request.form.get("name")
        student_id = request.form.get("student_id")
        record_parking(name, student_id)
        return redirect(url_for("parking_records"))

    return render_template("form.html")

def record_parking(name, student_id):
    current_datetime = datetime.now()
    date = datetime.now(timezone.utc)
    time = current_datetime.time()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO parking (name, student_id, date, time) VALUES (%s, %s, %s, %s) RETURNING id;", (name, student_id, date, time))
            record_id = cursor.fetchone()[0]

    return {
        "message": "Parking successful",
        "id": record_id,
        "NAME": name,
        "STUDENT ID": student_id,
        "PARKING DATE": date,
    }, 201

@app.route("/parking_records")
def parking_records():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, student_id, date, time FROM parking;")
            records = cursor.fetchall()
    return render_template("parking_records.html", records=records)




employee_data = [
    {
        "emp_id": "123451",
        "password": "pass1",
        "name": "Cyril Dabre",
        "salary": 100000.0,
    },
    {
        "emp_id": "123452",
        "password": "pass2",
        "name": "Russel Marti",
        "salary": 90000,
    },
    {
        "emp_id": "123453",
        "password": "pass3",
        "name": "Rency Marti",
        "salary": 120000,
    },
    {
        "emp_id": "123454",
        "password": "pass4",
        "name": "Thea Marti",
        "salary": 60000,
    },
    {
        "emp_id": "123455",
        "password": "pass5",
        "name": "Sam Boyd",
        "salary": 60000,
    },
]


def initialize_employees():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_EMPLOYEES_TABLE)
            for data in employee_data:
                cursor.execute(
                    INSERT_EMPLOYEE,
                    (data["emp_id"], data["password"], data["name"], data["salary"]),
                )


initialize_employees()


@app.route("/salary", methods=["GET", "POST"])
def salary_home():
    if request.method == "POST":
        emp_id = request.form.get("emp_id")
        password = request.form.get("password")
        return get_employee_salary(emp_id, password)
    return render_template("salary_form.html")


def get_employee_salary(emp_id, password):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_EMPLOYEE_SALARY, (emp_id, password))
            result = cursor.fetchone()

    if result:
        salary, name, emp_id = result
        return render_template("salary_result.html", emp_id=emp_id, name=name, salary=salary)
    else:
        return render_template("salary_result.html", message="No employee found with the given ID and password."), 404



@app.route("/register-course", methods=["GET", "POST"])
def register_course():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        course_name = request.form.get("course_name")
        student_name = request.form.get("student_name")
        semester = request.form.get("semester")
        course_id = add_course(student_id, course_name, student_name, semester)
        
        response_data = {
            "message": "Course registration successful",
            "Course ID": course_id,
            "Student ID": student_id,
            "Course Name": course_name,
            "Student Name": student_name,
            "Semester": semester
        }
        
        return render_template("course_response.html", response=response_data)

    return render_template("course_form.html")

def add_course(student_id, course_name, student_name, semester):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_COURSES_TABLE)
            cursor.execute(INSERT_COURSE, (student_id, course_name, student_name, semester))
            course_id = cursor.fetchone()[0]
    return course_id


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)









