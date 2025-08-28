import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from Main_Faculty import TeacherData
from image import get_text_from_image
import docx
import PyPDF2

def _gemini():
    api_key = 'YOUR_API_KEY'
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY env var.")
    return Gemini(id="gemini-2.0-flash", api_key=api_key)

Advise = Agent(
    model=_gemini(),
    instructions = dedent("""
    ### 1. **Input Understanding**
    Receive the following inputs:
    - Teacher Name
    - Subject taught
    - Average student grade in the subject (e.g., 0-100 scale)
    - Student feedback rating for the teacher (e.g., 1-5 scale)

    ### 2. **Performance Analysis**
    Analyze the inputs to assess:
    - Academic performance quality based on average grade
    - Teaching effectiveness and satisfaction based on feedback rating
    Identify if either or both metrics indicate weaknesses.

    ### 3. **Weakness Identification**
    Highlight the weakest link(s) by comparing inputs to ideal benchmarks:
    - Average grade below acceptable threshold (e.g., <70%)
    - Feedback rating below acceptable threshold (e.g., <3.5/5)
    Provide a clear explanation of the possible underlying causes.

    ### 4. **Actionable Recommendations**
    Suggest practical steps to improve performance, such as:
    - Enhancing teaching methods (e.g., interactive sessions, varied resources)
    - Increasing student engagement and motivation
    - Offering extra support or tutoring for struggling students
    - Seeking feedback and adjusting communication styles
    - Professional development or training opportunities

    ### 5. **Progress Tracking**
    Recommend measurable metrics and timeframes to evaluate improvements:
    - Target average grade improvements
    - Improvement in student feedback scores
    - Additional qualitative or quantitative measures

    ### 6. **Summary**
    Provide a concise summary emphasizing the key weakness and prioritized next steps to improve overall teaching effectiveness and student outcomes.
    """)
)

Advise_teacher = Agent(
    model=_gemini(),
    instructions = dedent("""
    ### 1. **Input Understanding**
    Receive the following inputs:
    - Student name
    - Last five exam marks (list of 5 integers, e.g., [78, 82, 75, 69, 88])
    - Last five days attendance (list of 5 entries, e.g., ['P', 'A', 'P', 'P', 'A'])

    ### 2. **Performance Evaluation**
    Assess the academic performance and engagement by:
    - Calculating the average exam score.
    - Calculating attendance percentage over the last 5 days.
    - Identifying performance trends (e.g., improving, declining, or inconsistent).

    ### 3. **Student Classification**
    Classify students based on performance:
    - **Top Performers**: High average marks (e.g., â‰¥85) and strong attendance (â‰¥80%)
    - **Consistent Performers**: Stable marks (70â€“84) and regular attendance (â‰¥60%)
    - **Needs Improvement**: Low marks (<70) and/or low attendance (<60%)
    Highlight students falling behind or showing inconsistent performance.

    ### 4. **Exam Weakness Identification**
    Analyze exam-wise performance across students:
    - Identify exams where the class average is significantly lower.
    - Mark such exams as focus areas for revision, re-teaching, or remedial classes.

    ### 5. **Actionable Class Insights**
    Provide actionable suggestions for class-wide improvement:
    - Focused revision on weaker exam topics.
    - Attendance encouragement strategies for low-attending students.
    - Peer mentoring by top performers for weaker students.
    - Short formative quizzes or feedback loops to monitor progress.

    ### 6. **Progress Monitoring**
    Suggest measurable ways to track progress:
    - Weekly attendance tracking and improvement targets.
    - Short weekly assessments and trend tracking.
    - Monthly review of average scores and comparison with past performance.

    ### 7. **Summary**
    Provide a summary including:
    - Class performance snapshot (average score, average attendance)
    - Top-performing students
    - Students needing attention
    - Key exams requiring more focus
    - Recommended next steps for class 
    
    
""")
)

Smart_Advise_student = Agent(
    model=_gemini(),
    instructions = dedent("""
    ### 1. **Input Details**
    Accept a block of **unstructured or semi-structured text** that may contain:
    - Exam scores (can appear as raw numbers, subject-wise entries, or informal text)
    - Academic topics or concepts (e.g., â€œlearned Photosynthesisâ€, â€œNewtonâ€™s Laws were toughâ€)

    The text can come from OCR, mixed notes, or file extractions and may not follow a fixed format.

    ### 2. **Data Parsing and Structuring**
    - **Extract Marks**:
        - Identify patterns like subject names followed by scores (e.g., â€œMaths - 75â€, â€œScience: 89â€, â€œEng 88â€)
        - If only raw numbers are present, infer context by grouping numbers into exam sets
        - Normalize to format: `[[subject1, mark1], [subject2, mark2], ...]` per exam
        
    - **Extract Topics**:
        - Detect mentioned topics or concepts (e.g., â€œQuadratic Equationsâ€, â€œPhotosynthesisâ€, â€œThermodynamicsâ€)
        - Compile a list of all unique topics found

    ### 3. **Performance Summary**
    - Show extracted marks for each exam, subject-wise
    - Calculate and display the **average score** across all exams and subjects
    - Identify **consistently strong or weak subjects** (based on repeated high/low scores)

    ### 4. **Performance Analysis**
    - Analyze trends:
        - **Improving**: Marks increasing over time
        - **Declining**: Marks dropping across exams
        - **Inconsistent**: Irregular pattern of highs and lows
    - Highlight subjects with **low or fluctuating performance**

    ### 5. **Topic Explanation**
    - List all identified topics
    - Provide a **1â€“2 line summary** or definition of each topic
    - Optionally tag the related subject (e.g., "Mitochondria â€“ Biology", "Algebra â€“ Mathematics")

    ### 6. **Student Categorization**
    Based on average exam performance:
    - **Excellent**: Average score â‰¥ 85
    - **Good**: 70 â‰¤ Average score < 85
    - **Needs Improvement**: Average score < 70

    ### 7. **Recommendations**
    Provide actionable suggestions based on analysis:
    - If average is low: Recommend focused study on weak subjects or topics
    - If trend is declining: Suggest revision schedule or concept reinforcement
    - Encourage topic-wise understanding and suggest resources or review sessions

    ### 8. **Summary Report**
    Generate a concise report that includes:
    - Subject-wise marks and average score
    - Trend analysis (improving, declining, inconsistent)
    - Weak subjects or topics
    - Topic explanations
    - Categorization (Excellent/Good/Needs Improvement)
    - Tailored recommendations for the student
""")

)

def advise_all_faculty():
    Fac, Att, Rat, Sub, Avg = TeacherData()
    data_all = {
        "faculty_names": Fac,
        "faculty_attendance_counts": Att,
        "faculty_ratings": Rat,
        "subjects": Sub,
        "avg_subject_marks_over_last5": Avg
    }
    
    ai_result = Advise.run(f"How is all faculty doing? {data_all}")
    # If ai_result is an object, try:
    if hasattr(ai_result, "text"):
        return ai_result.text
    elif hasattr(ai_result, "content"):
        return ai_result.content
    else:
        return str(ai_result)


def advise_teacher(data_marks: str, student_names: str, data_att: str):
    """Pass serialized strings or JSON from frontend."""
    prompt = f"How is my class doing? names={student_names} marks={data_marks} attendance={data_att}"
    return {"response": Advise_teacher.run(prompt)}

def smart_file_assist_from_text(text_block: str):
    return {"response": Smart_Advise_student.run(text_block)}

# ---------- File extraction helpers (no GUI) ----------
def extract_text_from_pdf(file_path: r"C:\Users\Admin\Downloads\Week_7_Report.pdf"):
    with open(file_path, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        return "\n".join([p.extract_text() or "" for p in reader.pages])

def extract_text_from_docx(file_path: r"C:\Users\Admin\Downloads\Week_7_Report.docx"):
    d = docx.Document(file_path)
    return "\n".join(p.text for p in d.paragraphs)

def smart_file_assist(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
        return smart_file_assist_from_text(text)
    if ext == ".docx":
        text = extract_text_from_docx(file_path)
        return smart_file_assist_from_text(text)
    if ext in [".png", ".jpg", ".jpeg", ".webp"]:
        res = get_text_from_image(file_path)
        text = res.get("text", str(res))
        return smart_file_assist_from_text(text)
    return {"error": "Unsupported file type. Use .pdf, .docx, .png/.jpg/.jpeg/.webp"}
