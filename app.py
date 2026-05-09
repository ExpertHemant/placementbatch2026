import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Placement Prediction System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# LOAD MODEL
# =========================
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# =========================
# CUSTOM CSS + HTML
# =========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e293b, #111827, #0f172a);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: white;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 10px;
    animation: fadeIn 2s ease-in-out;
}

.sub-title {
    text-align: center;
    font-size: 20px;
    color: #cbd5e1;
    margin-bottom: 30px;
    animation: fadeIn 3s ease-in-out;
}

.custom-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0px 8px 32px rgba(0,0,0,0.3);
    transition: 0.4s ease;
    animation: slideUp 1s ease;
}

.custom-card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0px 12px 40px rgba(0,0,0,0.5);
}

.result-success {
    background: linear-gradient(90deg, #16a34a, #22c55e);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    animation: pulse 1.5s infinite;
}

.result-fail {
    background: linear-gradient(90deg, #dc2626, #ef4444);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.03); }
    100% { transform: scale(1); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from { transform: translateY(60px); opacity: 0; }
    to { transform: translateY(0px); opacity: 1; }
}

div.stButton > button:first-child {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.8rem 2rem;
    font-size: 18px;
    font-weight: 600;
    transition: 0.4s;
    width: 100%;
}

div.stButton > button:first-child:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #1d4ed8, #6d28d9);
    box-shadow: 0px 8px 20px rgba(124,58,237,0.5);
}

.stNumberInput input {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="main-title">🚀 Placement Prediction System</div>
<div class="sub-title">AI Powered Student Placement Prediction Web App</div>
""", unsafe_allow_html=True)

# =========================
# FORM CONTAINER
# =========================
st.markdown('<div class="custom-card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    work_experience_months = st.number_input("Work Experience (Months)", 0, 120, 0)
    degree_percentage = st.number_input("Degree Percentage", 0.0, 100.0, 60.0)
    hsc_percentage = st.number_input("HSC Percentage", 0.0, 100.0, 60.0)
    technical_skills_score = st.number_input("Technical Skills Score", 0.0, 100.0, 50.0)
    ssc_percentage = st.number_input("SSC Percentage", 0.0, 100.0, 60.0)

with col2:
    has_work_experience = st.selectbox("Has Work Experience", [0, 1])
    soft_skills_score = st.number_input("Soft Skills Score", 0.0, 100.0, 50.0)
    communication_score = st.number_input("Communication Score", 0.0, 100.0, 50.0)
    total_score = st.number_input("Total Score", 0.0, 100.0, 60.0)
    internships_count = st.number_input("Internships Count", 0, 20, 0)

with col3:
    certifications_count = st.number_input("Certifications Count", 0, 50, 0)
    aptitude_score = st.number_input("Aptitude Score", 0.0, 100.0, 50.0)
    degree_field_Engineering = st.selectbox("Engineering Degree", [0, 1])
    city_tier_Tier_3 = st.selectbox("City Tier 3", [0, 1])
    backlogs = st.number_input("Backlogs", 0, 20, 0)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PREDICTION BUTTON
# =========================
if st.button("Predict Placement Status"):

    # ✅ Column names AND order exactly match model.feature_names_in_
    input_data = pd.DataFrame({
        'hsc_percentage': [hsc_percentage],
        'degree_percentage': [degree_percentage],
        'work_experience_months': [work_experience_months],
        'ssc_percentage': [ssc_percentage],
        'technical_skills_score': [technical_skills_score],
        'soft_skills_score': [soft_skills_score],
        'has_work_experience': [has_work_experience],
        'communication_score': [communication_score],
        'internships_count': [internships_count],
        'total_score': [total_score],
        'aptitude_score': [aptitude_score],
        'certifications_count': [certifications_count],
        'degree_field_Engineering': [degree_field_Engineering],
        'city_tier_Tier 3': [city_tier_Tier_3],   # ✅ space, not underscore
        'backlogs': [backlogs]
    })

    with st.spinner("Analyzing Student Profile..."):
        time.sleep(2)

    try:
        prediction = model.predict(input_data)[0]
    except ValueError as e:
        st.error(f"Feature mismatch error: {e}")
        st.write("Expected features by model:", list(model.feature_names_in_))
        st.write("Features you passed:", list(input_data.columns))
        st.stop()

    try:
        probability = model.predict_proba(input_data)[0][1] * 100
    except:
        probability = None

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # RESULT
    # =========================
    if prediction == 1:
        prob_text = f"<br><br>Confidence Score: {probability:.2f}%" if probability is not None else ""
        st.markdown(f"""
        <div class="result-success">
            🎉 Student is Likely to be Placed
            {prob_text}
        </div>
        """, unsafe_allow_html=True)
    else:
        prob_text = f"<br><br>Confidence Score: {probability:.2f}%" if probability is not None else ""
        st.markdown(f"""
        <div class="result-fail">
            ❌ Student is Less Likely to be Placed
            {prob_text}
        </div>
        """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<br><br>
<hr style="border:1px solid #334155">
<div style='text-align:center; color:#94a3b8; font-size:16px;'>
    Built with ❤️ using Streamlit & Scikit-Learn 1.6.1
</div>
""", unsafe_allow_html=True)