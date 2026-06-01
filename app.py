import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
from database import create_database, create_table, add_patient, get_all_patients, update_patient, delete_patient
from ai_helper import get_health_remarks

# Initialize database
create_database()
create_table()

# Page config
st.set_page_config(page_title="MIRA Health Prediction", page_icon="🏥", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .main { background-color: #0a0e1a; }
    .stApp { background-color: #0a0e1a; }
    
    .title-box {
        background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 50%, #00c853 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(26, 115, 232, 0.4);
    }
    
    .title-box h1 {
        font-size: 2.8em !important;
        font-weight: 700;
        margin: 0;
        letter-spacing: 2px;
    }
    
    .title-box p {
        font-size: 1.2em;
        opacity: 0.9;
        margin-top: 10px;
    }
    
    .card {
        background: linear-gradient(135deg, #1a1f35, #0d1526);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #1a73e8;
        box-shadow: 0 4px 20px rgba(26, 115, 232, 0.2);
        margin-bottom: 20px;
        color: white;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: 700;
        color: #00c853;
    }
    
    .metric-label {
        font-size: 1em;
        opacity: 0.8;
        margin-top: 5px;
    }

    .risk-high {
        background: linear-gradient(135deg, #c62828, #b71c1c);
        padding: 8px 16px;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        font-size: 0.9em;
        display: inline-block;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f57f17, #e65100);
        padding: 8px 16px;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        font-size: 0.9em;
        display: inline-block;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #2e7d32, #1b5e20);
        padding: 8px 16px;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        font-size: 0.9em;
        display: inline-block;
    }

    .remarks-box {
        background: linear-gradient(135deg, #0d1f3c, #0a1628);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #00c853;
        color: #e0e0e0;
        font-size: 1.1em;
        line-height: 1.8;
        white-space: pre-line;
        margin-top: 15px;
    }

    .stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label {
        font-size: 1.1em !important;
        font-weight: 600 !important;
        color: #90caf9 !important;
    }

    .stTextInput input, .stNumberInput input {
        font-size: 1.1em !important;
        background-color: #1a1f35 !important;
        color: white !important;
        border: 1px solid #1a73e8 !important;
        border-radius: 8px !important;
    }

    h1, h2, h3 {
        color: white !important;
        font-size: 1.8em !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #1a73e8, #00c853) !important;
        color: white !important;
        font-size: 1.1em !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.4) !important;
    }

    .stDataFrame {
        font-size: 1.1em !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1526, #1a1f35) !important;
        border-right: 1px solid #1a73e8;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
        font-size: 1.1em !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
    <div class="title-box">
        <h1>🏥 MIRA Health Prediction</h1>
        <p>Medical Intelligence Robotic Automation — AI-Powered Patient Health Analysis</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 🏥 MIRA Navigation")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox("📋 Select Option",
    ["🏠 Dashboard", "➕ Add Patient", "✏️ Update Patient", "🗑️ Delete Patient"])
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Info")
data = get_all_patients()
st.sidebar.markdown(f"👥 **Total Patients:** {len(data)}")
st.sidebar.markdown(f"📅 **Date:** {date.today().strftime('%d %b %Y')}")
st.sidebar.markdown(f"🤖 **AI Status:** 🟢 Active")

# Helper: Risk Level
def get_risk_level(glucose, cholesterol, haemoglobin):
    risk = 0
    if glucose > 180: risk += 2
    elif glucose > 120: risk += 1
    if cholesterol > 280: risk += 2
    elif cholesterol > 200: risk += 1
    if haemoglobin < 8: risk += 2
    elif haemoglobin < 11: risk += 1
    if risk >= 4: return "🔴 High Risk"
    elif risk >= 2: return "🟡 Medium Risk"
    else: return "🟢 Low Risk"

# ==================== DASHBOARD ====================
if menu == "🏠 Dashboard":
    st.markdown("## 📊 Patient Dashboard")

    if data:
        df = pd.DataFrame(data, columns=["ID", "Full Name", "Date of Birth",
                                          "Email", "Glucose", "Haemoglobin",
                                          "Cholesterol", "Remarks"])

        # Stats Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{len(data)}</div>
                <div class="metric-label">👥 Total Patients</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            avg_glucose = round(df["Glucose"].mean(), 1)
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{avg_glucose}</div>
                <div class="metric-label">🩸 Avg Glucose</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            avg_chol = round(df["Cholesterol"].mean(), 1)
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{avg_chol}</div>
                <div class="metric-label">🫀 Avg Cholesterol</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            avg_hemo = round(df["Haemoglobin"].mean(), 1)
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{avg_hemo}</div>
                <div class="metric-label">💉 Avg Haemoglobin</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Risk Level Column
        df["Risk Level"] = df.apply(lambda row: get_risk_level(
            row["Glucose"], row["Cholesterol"], row["Haemoglobin"]), axis=1)

        # Charts Row
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📈 Blood Test Comparison")
            fig = px.bar(df, x="Full Name",
                        y=["Glucose", "Haemoglobin", "Cholesterol"],
                        barmode="group",
                        color_discrete_sequence=["#1a73e8", "#00c853", "#ff6d00"],
                        template="plotly_dark")
            fig.update_layout(
                plot_bgcolor="#0d1526",
                paper_bgcolor="#0d1526",
                font=dict(color="white", size=13),
                legend=dict(font=dict(size=13)),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 🎯 Risk Level Distribution")
            risk_counts = df["Risk Level"].value_counts().reset_index()
            risk_counts.columns = ["Risk Level", "Count"]
            fig2 = px.pie(risk_counts, values="Count", names="Risk Level",
                         color_discrete_sequence=["#00c853", "#ff6d00", "#c62828"],
                         template="plotly_dark")
            fig2.update_layout(
                plot_bgcolor="#0d1526",
                paper_bgcolor="#0d1526",
                font=dict(color="white", size=13),
                height=350
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### 👥 Patient Records")
        display_df = df[["ID", "Full Name", "Date of Birth", "Email",
                         "Glucose", "Haemoglobin", "Cholesterol", "Risk Level"]]
        st.dataframe(display_df, use_container_width=True)

    else:
        st.info("No patients found. Please add a patient first.")

# ==================== ADD ====================
elif menu == "➕ Add Patient":
    st.markdown("## ➕ Add New Patient")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("👤 Full Name")
        dob = st.date_input("📅 Date of Birth",
                           min_value=date(1900, 1, 1),
                           max_value=date.today())
        email = st.text_input("📧 Email Address")
    with col2:
        glucose = st.number_input("🩸 Glucose (mg/dL)", min_value=0.0)
        haemoglobin = st.number_input("💉 Haemoglobin (g/dL)", min_value=0.0)
        cholesterol = st.number_input("🫀 Cholesterol (mg/dL)", min_value=0.0)

    st.markdown("---")

    if st.button("🔍 Generate AI Remarks & Save", use_container_width=True):
        if not full_name:
            st.error("⚠️ Please enter Full Name!")
        elif not email or "@" not in email:
            st.error("⚠️ Please enter a valid Email Address!")
        elif glucose <= 0 or haemoglobin <= 0 or cholesterol <= 0:
            st.error("⚠️ Blood test values must be greater than 0!")
        else:
            with st.spinner("🤖 Generating AI health remarks..."):
                remarks = get_health_remarks(glucose, haemoglobin, cholesterol)
            add_patient(full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
            risk = get_risk_level(glucose, cholesterol, haemoglobin)
            st.success("✅ Patient added successfully!")
            st.markdown(f"### Risk Level: {risk}")
            st.markdown(f'<div class="remarks-box">🤖 <b>AI Health Remarks:</b><br><br>{remarks}</div>',
                       unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== UPDATE ====================
elif menu == "✏️ Update Patient":
    st.markdown("## ✏️ Update Patient Record")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    data = get_all_patients()
    if data:
        patient_options = {f"ID {row[0]} — {row[1]}": row[0] for row in data}
        selected_name = st.selectbox("🔎 Select Patient", list(patient_options.keys()))
        selected_id = patient_options[selected_name]
        selected = next(row for row in data if row[0] == selected_id)

        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("👤 Full Name", value=selected[1])
            dob = st.date_input("📅 Date of Birth", value=selected[2],
                               min_value=date(1900, 1, 1), max_value=date.today())
            email = st.text_input("📧 Email Address", value=selected[3])
        with col2:
            glucose = st.number_input("🩸 Glucose (mg/dL)", min_value=0.0, value=float(selected[4]))
            haemoglobin = st.number_input("💉 Haemoglobin (g/dL)", min_value=0.0, value=float(selected[5]))
            cholesterol = st.number_input("🫀 Cholesterol (mg/dL)", min_value=0.0, value=float(selected[6]))

        if st.button("🔍 Regenerate Remarks & Update", use_container_width=True):
            if not full_name:
                st.error("⚠️ Please enter Full Name!")
            elif not email or "@" not in email:
                st.error("⚠️ Please enter a valid Email Address!")
            elif glucose <= 0 or haemoglobin <= 0 or cholesterol <= 0:
                st.error("⚠️ Blood test values must be greater than 0!")
            else:
                with st.spinner("🤖 Generating AI health remarks..."):
                    remarks = get_health_remarks(glucose, haemoglobin, cholesterol)
                update_patient(selected_id, full_name, dob, email,
                             glucose, haemoglobin, cholesterol, remarks)
                risk = get_risk_level(glucose, cholesterol, haemoglobin)
                st.success("✅ Patient updated successfully!")
                st.markdown(f"### Risk Level: {risk}")
                st.markdown(f'<div class="remarks-box">🤖 <b>AI Health Remarks:</b><br><br>{remarks}</div>',
                           unsafe_allow_html=True)
    else:
        st.info("No patients found. Please add a patient first.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== DELETE ====================
elif menu == "🗑️ Delete Patient":
    st.markdown("## 🗑️ Delete Patient Record")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    data = get_all_patients()
    if data:
        patient_options = {f"ID {row[0]} — {row[1]}": row[0] for row in data}
        selected_name = st.selectbox("🔎 Select Patient to Delete", list(patient_options.keys()))
        selected_id = patient_options[selected_name]
        selected = next(row for row in data if row[0] == selected_id)

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"👤 **Name:** {selected[1]}")
        with col2:
            st.markdown(f"📧 **Email:** {selected[3]}")
        with col3:
            st.markdown(f"📅 **DOB:** {selected[2]}")
        st.markdown("---")

        if st.button("🗑️ Confirm Delete", use_container_width=True):
            delete_patient(selected_id)
            st.success("✅ Patient deleted successfully!")
    else:
        st.info("No patients found. Please add a patient first.")
    st.markdown('</div>', unsafe_allow_html=True)