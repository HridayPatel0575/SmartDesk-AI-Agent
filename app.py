from flask import Flask, request, jsonify, render_template
from File_Management import Attendance_Entry, Marks_Entry
from Students import marks_check_1, att_check_1, get_last_five_exam_marks
from Main_Faculty import Faculty_Att, Faculty_Rating
from SelectFun import advise_all_faculty, advise_teacher, smart_file_assist
import os
from flask import Flask, request, jsonify, render_template, session


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey123")

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/faculty")
def faculty_page():
    return render_template("faculty.html")

@app.get("/student")
def student_page():
    return render_template("student.html")

@app.get("/file")
def file_page():
    return render_template("file.html")


@app.post("/faculty/attendance")
def submit_attendance():
    data = request.json
    return jsonify(Attendance_Entry(
        data["faculty_code"],
        data["attendance_data"],
        data.get("date")
    ))

@app.post("/faculty/marks")
def submit_marks():
    data = request.json
    return jsonify(Marks_Entry(
        data["faculty_code"],
        data["exam_number"],
        data["marks_data"],
        data.get("date")
    ))

@app.get("/faculty/last5/marks/<int:code>")
def last5_marks_faculty(code):
    return jsonify(get_last_five_exam_marks(code))

@app.get("/faculty/last5/attendance/<int:code>")
def last5_att_faculty(code):
    return jsonify(Faculty_Att(code))

@app.get("/faculty/overview")
def faculty_overview():
    return jsonify({"response": advise_all_faculty()})



@app.post("/student/login")
def student_login():
    data = request.get_json()   # ✅ safer than request.json
    ID, pw = data["id"], data["password"]
    from File_Management import credentials
    if credentials.get(ID) == pw:
        session["student_id"] = ID
        return jsonify({"status": "success", "id": ID})
    return jsonify({"status": "failed", "reason": "Invalid credentials"})





@app.post("/student/marks_by_date")
def student_marks_by_date():
    if "student_id" not in session:
        return jsonify({"error": "Login required"}), 401
    data = request.json
    return jsonify(marks_check_1(session["student_id"], data["date"]))

@app.post("/student/attendance_history")
def student_attendance_history():
    if "student_id" not in session:
        return jsonify({"error": "Login required"}), 401
    return jsonify(att_check_1(session["student_id"]))

@app.post("/student/last5_marks")
def student_last5_marks():
    if "student_id" not in session:
        return jsonify({"error": "Login required"}), 401
    return jsonify(get_last_five_exam_marks(session["student_id"]))

@app.post("/student/logout")
def student_logout():
    session.pop("student_id", None)
    return jsonify({"status": "success", "message": "Logged out successfully"})

@app.post("/advise/teacher")
def advise_teacher_route():
    data = request.json
    return jsonify({"response": advise_teacher(
        data["marks"], data["names"], data["attendance"]
    )})


@app.post("/assist/file")
def assist_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    try:
        result = smart_file_assist(filepath)
        return jsonify({"response": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == "__main__":
    app.run(debug=True)
