import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the trained model
model = joblib.load("/content/drive/MyDrive/Colab_Notebooks/AcadOptimizer/models/final_model.pkl")

st.title("🎓 ACAD Optimizer - Student Performance Predictor")
st.write("Upload your details or enter manually to check your predicted GPA and attendance insights.")

# Create input fields for model features
semester = st.number_input("Semester", min_value=1, max_value=8, step=1)
total_classes = st.number_input("Total Classes", min_value=1, step=1)
attended_classes = st.number_input("Attended Classes", min_value=0, step=1)
midterm_marks = st.number_input("Midterm Marks", min_value=0, max_value=100)
assignment_marks = st.number_input("Assignment Marks", min_value=0, max_value=100)
quiz_marks = st.number_input("Quiz Marks", min_value=0, max_value=100)
internal_marks = st.number_input("Internal Marks", min_value=0, max_value=100)
final_exam_marks = st.number_input("Final Exam Marks", min_value=0, max_value=100)
attendance_percent = (attended_classes / total_classes) * 100 if total_classes > 0 else 0
study_hours_per_day = st.number_input("Study Hours per Day", min_value=0.0, max_value=12.0)
participation_score = st.number_input("Participation Score", min_value=0, max_value=10)
previous_sem_gpa = st.number_input("Previous Semester GPA", min_value=0.0, max_value=10.0)

# Derived features
missing_classes = total_classes - attended_classes
performance_score = midterm_marks + assignment_marks + quiz_marks + internal_marks

# Collect data
input_data = pd.DataFrame([[
    semester, total_classes, attended_classes, missing_classes,
    midterm_marks, assignment_marks, quiz_marks, internal_marks,
    final_exam_marks, attendance_percent, study_hours_per_day,
    participation_score, previous_sem_gpa, performance_score
]], columns=[
    "semester", "total_classes", "attended_classes", "missing_classes",
    "midterm_marks", "assignment_marks", "quiz_marks", "internal_marks",
    "final_exam_marks", "attendance_percent", "study_hours_per_day",
    "participation_score", "previous_sem_gpa", "performance_score"
])

# Predict when button is pressed
if st.button("Predict Performance"):
    prediction = model.predict(input_data)[0]
    st.success(f"🎯 Predicted Final GPA: {prediction:.2f}")

    # Attendance insight
    if attendance_percent < 75:
        required_classes = np.ceil((0.75 * total_classes - attended_classes) / 0.25)
        st.warning(f"⚠️ You need to attend approximately {required_classes} more classes to reach 75% attendance.")
    else:
        st.info("✅ Your attendance is already above 75%!")

st.caption("Developed by Palak Khare , Surabhi, Anvesha Srivastava | AcadOptimizer")
