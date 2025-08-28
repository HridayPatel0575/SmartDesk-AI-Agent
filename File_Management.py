# File_Management.py
import datetime
import os
import csv
import pandas as pd
from Main_Faculty import get_last_five_files, get_last_five_files_Att

now = datetime.datetime.now()
now1 = now.strftime("%d-%m-%Y")
stripped_date = now1.replace("-", "")
ATT_DIR = r'C:\Users\Admin\Desktop\internship reports\Attendance'
GRD_DIR = r'C:\Users\Admin\Desktop\internship reports\Grade'
file_path_att = fr'{ATT_DIR}\Attendance{stripped_date}.csv'
file_path_grd = fr'{GRD_DIR}\Grade{stripped_date}.csv'

fieldnames = ['Name', 'Maths', 'Physics', 'Chemistry', 'English', 'Computer']

student_names = [
    "Aarav Patel", "Vivaan Sharma", "Aditya Verma", "Vihaan Mehta", "Arjun Reddy",
    "Sai Iyer", "Reyansh Nair", "Krishna Das", "Ishaan Mishra", "Dhruv Yadav",
    "Atharv Singh", "Aryan Thakur", "Kartik Joshi", "Rudra Saxena", "Ayaan Bhatia",
    "Om Shukla", "Yuvraj Jha", "Ansh Raj", "Shivam Pandey", "Harsh Choudhary",
    "Neha Sharma", "Ananya Iyer", "Aanya Mehta", "Diya Verma", "Ishita Reddy",
    "Saanvi Das", "Tanya Patel", "Kritika Bansal", "Riya Yadav", "Navya Singh",
    "Meera Jha", "Shruti Saxena", "Prisha Kapoor", "Avni Mishra", "Kiara Thakur",
    "Anika Joshi", "Pihu Bhatia", "Simran Raj", "Suhana Shukla", "Jhanvi Nair",
    "Tanvi Pandey", "Muskan Choudhary", "Sneha Sharma", "Nitya Iyer", "Vanya Mehta",
    "Trisha Verma", "Mahira Reddy", "Radhika Das", "Ira Bansal", "Myra Singh"
]

credentials = {f'23aiml{i:03}': f'p{i:03}' for i in range(1, 51)}

id_to_name = {
    '23aiml001': 'Aarav Patel','23aiml002': 'Vivaan Sharma','23aiml003': 'Aditya Verma','23aiml004': 'Vihaan Mehta',
    '23aiml005': 'Arjun Reddy','23aiml006': 'Sai Iyer','23aiml007': 'Reyansh Nair','23aiml008': 'Krishna Das',
    '23aiml009': 'Ishaan Mishra','23aiml010': 'Dhruv Yadav','23aiml011': 'Atharv Singh','23aiml012': 'Aryan Thakur',
    '23aiml013': 'Kartik Joshi','23aiml014': 'Rudra Saxena','23aiml015': 'Ayaan Bhatia','23aiml016': 'Om Shukla',
    '23aiml017': 'Yuvraj Jha','23aiml018': 'Ansh Raj','23aiml019': 'Shivam Pandey','23aiml020': 'Harsh Choudhary',
    '23aiml021': 'Neha Sharma','23aiml022': 'Ananya Iyer','23aiml023': 'Aanya Mehta','23aiml024': 'Diya Verma',
    '23aiml025': 'Ishita Reddy','23aiml026': 'Saanvi Das','23aiml027': 'Tanya Patel','23aiml028': 'Kritika Bansal',
    '23aiml029': 'Riya Yadav','23aiml030': 'Navya Singh','23aiml031': 'Meera Jha','23aiml032': 'Shruti Saxena',
    '23aiml033': 'Prisha Kapoor','23aiml034': 'Avni Mishra','23aiml035': 'Kiara Thakur','23aiml036': 'Anika Joshi',
    '23aiml037': 'Pihu Bhatia','23aiml038': 'Simran Raj','23aiml039': 'Suhana Shukla','23aiml040': 'Jhanvi Nair',
    '23aiml041': 'Tanvi Pandey','23aiml042': 'Muskan Choudhary','23aiml043': 'Sneha Sharma','23aiml044': 'Nitya Iyer',
    '23aiml045': 'Vanya Mehta','23aiml046': 'Trisha Verma','23aiml047': 'Mahira Reddy','23aiml048': 'Radhika Das',
    '23aiml049': 'Ira Bansal','23aiml050': 'Myra Singh'
}

fac_map = {1: 'Maths', 2: 'Physics', 3: 'Chemistry', 4: 'English', 5: 'Computer'}

# Pre-load last-5 file lists
a = get_last_five_files(GRD_DIR)
b = get_last_five_files_Att(ATT_DIR)


def _ensure_table(file_path: str):
    """Ensure CSV exists with header & 50 students."""
    exists = os.path.exists(file_path)
    data = {}
    if exists:
        with open(file_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            data = {row['Name']: row for row in reader}
    else:
        data = {name: {fn: '' for fn in fieldnames} for name in student_names}
        for s in student_names:
            data[s]['Name'] = s
    return data


def Attendance_Entry(faculty_code: int, attendance_data: dict, target_date: str = None):
    """
    attendance_data = {'Aarav Patel': 'P', ...}
    target_date: 'DD/MM/YYYY' (optional) if you want to write a specific date file.
    """
    subject = fac_map.get(faculty_code)
    if not subject:
        return {"error": "Invalid faculty code."}

    if target_date:
        fname = target_date.replace("/", "")
        path = fr'{ATT_DIR}\Attendance{fname}.csv'
    else:
        path = file_path_att

    table = _ensure_table(path)

    for name, status in attendance_data.items():
        if name in table:
            table[name][subject] = status

    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in table.values():
            writer.writerow(row)

    return {"message": f"Attendance updated for {subject}", "file": path}


def Marks_Entry(faculty_code: int, exam_number: int, marks_data: dict, target_date: str = None):
    """
    marks_data = {'Aarav Patel': 78, ...}
    """
    subject = fac_map.get(faculty_code)
    if not subject:
        return {"error": "Invalid faculty code."}
    if not (1 <= exam_number <= 5):
        return {"error": "Invalid exam number. Must be 1–5."}

    if target_date:
        fname = target_date.replace("/", "")
        path = fr'{GRD_DIR}\Grade{fname}.csv'
    else:
        path = file_path_grd

    table = _ensure_table(path)

    for name, marks in marks_data.items():
        if name in table:
            table[name][subject] = marks

    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in table.values():
            writer.writerow(row)

    return {"message": f"Marks updated for {subject}, Exam {exam_number}", "file": path}


def Attendance_check(date_ddmmyyyy: str):
    fname = date_ddmmyyyy.replace("/", "")
    path = fr'{ATT_DIR}\Attendance{fname}.csv'
    return {"file": path} if os.path.exists(path) else {"error": "No Data"}


def Grade_check(date_ddmmyyyy: str):
    fname = date_ddmmyyyy.replace("/", "")
    path = fr'{GRD_DIR}\Grade{fname}.csv'
    return {"file": path} if os.path.exists(path) else {"error": "No Data"}


def get_last_5_subject_marks(faculty_code: int):
    subject = fac_map.get(faculty_code)
    if not subject:
        return {"error": "Invalid faculty code."}
    selected = a[-5:]
    all_marks = []
    for p in selected:
        try:
            df = pd.read_csv(p)
            all_marks.append(df[subject].tolist() if subject in df.columns else [])
        except Exception:
            all_marks.append([])
    return {"subject": subject, "marks": all_marks, "files": [os.path.basename(x) for x in selected]}


def get_last_5_att(faculty_code: int):
    subject = fac_map.get(faculty_code)
    if not subject:
        return {"error": "Invalid faculty code."}
    selected = b[-5:]
    all_att = []
    for p in selected:
        try:
            df = pd.read_csv(p)
            all_att.append(df[subject].tolist() if subject in df.columns else [])
        except Exception:
            all_att.append([])
    return {"subject": subject, "attendance": all_att, "files": [os.path.basename(x) for x in selected]}
