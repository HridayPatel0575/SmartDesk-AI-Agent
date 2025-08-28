# Main_Faculty.py
import pandas as pd
import statistics
import os

GRADE_DIR = r'C:\Users\Admin\Desktop\internship reports\Grade'
ATT_DIR = r'C:\Users\Admin\Desktop\internship reports\Attendance'

def get_last_five_files(folder_path, extension=".csv"):
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith(extension)]
        files_full = [os.path.join(folder_path, f) for f in files]
        files_sorted = sorted(files_full, key=os.path.getmtime, reverse=True)
        return files_sorted[:5]
    except Exception:
        return []

def get_last_five_files_Att(folder_path_1, extension='.csv'):
    try:
        files = [f for f in os.listdir(folder_path_1) if f.endswith(extension)]
        files_full = [os.path.join(folder_path_1, f) for f in files]
        files_sorted = sorted(files_full, key=os.path.getmtime, reverse=True)
        return files_sorted[:5]
    except Exception:
        return []

a = get_last_five_files(GRADE_DIR)
b = get_last_five_files_Att(ATT_DIR)

def Faculty_Att(Fac):
    try:
        Data_Att = pd.read_csv(r"C:\Users\Admin\Downloads\faculty_attendance.csv")
        present = Data_Att[Fac].tolist().count('P')
        return f"{present} / 30"
    except Exception as e:
        return f"Attendance error: {e}"

def Faculty_Rating(Fac):
    try:
        Data_Rat = pd.read_csv(r"C:\Users\Admin\Downloads\faculty_feedback.csv")
        Rat = statistics.mean(Data_Rat[Fac].tolist())
        return f"{Rat} / 5"
    except Exception as e:
        return f"Rating error: {e}"

def Avg_Marks_Per_Subject():
    files = get_last_five_files(GRADE_DIR)
    if not files:
        return [0, 0, 0, 0, 0]

    buckets = {"Maths": [], "Physics": [], "Chemistry": [], "English": [], "Computer": []}
    for fp in files:
        try:
            df = pd.read_csv(fp)
            for col in buckets.keys():
                s = pd.to_numeric(df[col], errors='coerce').dropna()
                if not s.empty:
                    buckets[col].append(s.mean())
        except Exception:
            continue

    return [statistics.mean(buckets[k]) if buckets[k] else 0 for k in ["Maths","Physics","Chemistry","English","Computer"]]

def TeacherData():
    Fac = ['Jay','Neha','Amit','Sneha','Rahul']
    Sub = ['Maths','Physics','Chemistry','English','Computer']
    Att, Rat1 = [], []
    Avg = Avg_Marks_Per_Subject()
    Data_Att = pd.read_csv(r"C:\Users\Admin\Downloads\faculty_attendance.csv")
    Data_Rat = pd.read_csv(r"C:\Users\Admin\Downloads\faculty_feedback.csv")
    for name in Fac:
        Att.append(Data_Att[name].tolist().count('P'))
        Rat1.append(statistics.mean(Data_Rat[name].tolist()))
    return Fac, Att, Rat1, Sub, Avg
