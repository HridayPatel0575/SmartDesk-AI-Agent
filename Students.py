# Students.py
import os
import pandas as pd
from File_Management import id_to_name, credentials
from Main_Faculty import get_last_five_files, get_last_five_files_Att

GRD_DIR = r'C:\Users\Admin\Desktop\internship reports\Grade'
ATT_DIR = r'C:\Users\Admin\Desktop\internship reports\Attendance'

a = get_last_five_files(GRD_DIR)
b = get_last_five_files_Att(ATT_DIR)

def validate_login(student_id: str, password: str):
    if student_id in credentials and credentials[student_id] == password:
        return {"ok": True}
    return {"ok": False, "error": "Invalid ID or Password."}

def marks_check_1(ID, date_ddmmyyyy: str):
    fname = date_ddmmyyyy.replace("/", "")
    path = fr'{GRD_DIR}\Grade{fname}.csv'
    if not os.path.exists(path):
        return {"error": "No Data for this date."}

    student_name = id_to_name.get(ID)
    if not student_name:
        return {"error": "Invalid student ID."}

    df = pd.read_csv(path)
    if student_name in df['Name'].values:
        row = df[df['Name'] == student_name]
        return {"date": date_ddmmyyyy, "student": student_name, "marks": row.to_dict(orient="records")[0]}
    else:
        return {"error": f"No marks found for {student_name} on this date."}

def att_check_1(ID):
    student_name = id_to_name.get(ID)
    if not student_name:
        return {"error": "Invalid student ID."}

    last_5 = b[-5:]
    recs = []
    for p in last_5:
        try:
            df = pd.read_csv(p)
            date_token = os.path.basename(p).split("Attendance")[-1].split(".csv")[0]
            status_row = df[df['Name'].str.strip() == student_name.strip()]
            if not status_row.empty:
                # assumes second column is the aggregated attendance per subject day-wise
                att_value = status_row.iloc[0, 1]
                recs.append({"date": date_token, "status": att_value})
        except Exception:
            continue
    return {"student": student_name, "attendance": recs}

def get_last_five_exam_marks(ID):
    files = sorted(a)[-5:]
    out = []
    student_name = id_to_name.get(ID)
    if not student_name:
        return {"error": "Invalid student ID."}

    for p in files:
        try:
            df = pd.read_csv(p)
            row = df[df['Name'].str.strip() == student_name.strip()]
            if not row.empty:
                out.append({"file": os.path.basename(p), "marks": row.iloc[0].drop('Name').to_dict()})
        except Exception:
            continue
    return {"student": student_name, "marks": out}
