# Import libraries
import streamlit as st
import joblib
import pandas as pd
from datetime import datetime, timedelta

# Load models
maternal_health_model = joblib.load('maternal_health_model.pkl')
model_regularity = joblib.load('model_regularity (1).pkl')
model_ovulation = joblib.load('model_ovulation (1).pkl')
mental_health_model = joblib.load('women_mental_health_model.pkl')

# Define prediction functions for maternal health
def predict_risk(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate):
    input_data = pd.DataFrame({
        'Age': [age],
        'SystolicBP': [systolic_bp],
        'DiastolicBP': [diastolic_bp],
        'BS': [bs],
        'BodyTemp': [body_temp],
        'HeartRate': [heart_rate]
    })
    prediction = maternal_health_model.predict(input_data)
    risk_levels = {0: 'Low Risk', 1: 'Mid Risk', 2: 'High Risk'}
    return risk_levels[prediction[0]]

def get_maternal_recommendation(risk_level):
    if risk_level == 'Low Risk':
        return "Maintain a healthy lifestyle. Regular check-ups are recommended."
    elif risk_level == 'Mid Risk':
        return "Monitor your health closely. Consult a doctor if symptoms worsen."
    else:
        return "Seek immediate medical attention. Follow your doctor’s advice."

# Function to calculate the next cycle date
def calculate_next_cycle_date(start_date, cycle_length):
    return start_date + timedelta(days=cycle_length)

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Main background color */
    .stApp {
        background-color: #FFB4A2;
        color: #333333;
    }
    /* Sidebar background color */
    .css-1d391kg {
        background-color: #B7B1F2 !important;
    }
    /* Button styling */
    .stButton>button {
        background-color: #a8e6cf;
        color: #333333;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #dcedc1;
    }
    /* Input field styling */
    .stNumberInput>div>div>input, .stSelectbox>div>div>select, .stMultiselect>div>div>div {
        background-color: #ffd3b6;
        color: #333333;
    }
    /* Success and warning message styling */
    .stSuccess {
        background-color: #dcedc1;
        color: #333333;
        padding: 10px;
        border-radius: 10px;
    }
    .stWarning {
        background-color: #ffaaa5;
        color: #333333;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set up the sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Maternal Health", "Menstrual Cycle", "Mental Well-being"])

# Home Page
if page == "Home":
    st.title("🌸 Women's Health Dashboard 🌸")
    st.write("Welcome to the Women's Health Dashboard! Use the sidebar to navigate to different sections.")
    
    # Add an image
    st.image("image1.jpg", caption="Empowering Women Through Health Awareness")

# Maternal Health Page
elif page == "Maternal Health":
    st.title("🤰 Maternal Health Predictor")
    st.write("Enter your details to predict maternal health risks.")

    # Input fields
    age = st.number_input("Age", min_value=10, max_value=50, value=25)
    systolic_bp = st.number_input("Systolic Blood Pressure", min_value=50, max_value=200, value=120)
    diastolic_bp = st.number_input("Diastolic Blood Pressure", min_value=30, max_value=150, value=80)
    bs = st.number_input("Blood Sugar Level", min_value=2.0, max_value=20.0, value=5.0)
    body_temp = st.number_input("Body Temperature", min_value=35.0, max_value=42.0, value=37.0)
    heart_rate = st.number_input("Heart Rate", min_value=50, max_value=150, value=80)

    # Predict button
    if st.button("Predict"):
        risk_level = predict_risk(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate)
        recommendation = get_maternal_recommendation(risk_level)
        st.success(f"Predicted Risk Level: {risk_level}")
        st.write(f"Recommendation: {recommendation}")

# Menstrual Cycle Page
elif page == "Menstrual Cycle":
    st.title("📅 Menstrual Cycle Predictor")
    st.write("Enter your details to predict menstrual cycle regularity, ovulation date, and next cycle date.")

    # Input fields
    age = st.number_input("Age", min_value=10, max_value=50, value=25)
    cycle_length = st.number_input("Cycle Length (in days)", min_value=20, max_value=40, value=28)
    cycle_start_day = st.number_input("Cycle Start Day", min_value=1, max_value=31, value=15)
    cycle_start_month = st.number_input("Cycle Start Month", min_value=1, max_value=12, value=5)
    cycle_start_year = st.number_input("Cycle Start Year", min_value=2000, max_value=2100, value=2023)

    # Symptoms dropdown
    symptoms = st.multiselect(
        "Select your symptoms",
        ["Cramps", "Fatigue", "Vomiting/Nausea", "Headache", "Mood Swings", 
         "Bloating", "Back Pain", "Breast Tenderness", "Food Cravings", "Insomnia"]
    )

    # Predict button
    if st.button("Predict"):
        # Prepare input data
        input_data = [[
            age,               # age
            1,                 # cycle_number (hardcoded as 1)
            cycle_length,      # cycle_length
            cycle_start_day,   # cycle_start_day
            cycle_start_month, # cycle_start_month
            cycle_start_year   # cycle_start_year
        ]]

        # Make predictions
        regularity_pred = model_regularity.predict(input_data)
        ovulation_pred = model_ovulation.predict(input_data)

        # Calculate next cycle date
        start_date = datetime(year=cycle_start_year, month=cycle_start_month, day=cycle_start_day)
        next_cycle_date = calculate_next_cycle_date(start_date, cycle_length)

        # Calculate ovulation date
        ovulation_date = next_cycle_date - timedelta(days=ovulation_pred[0])

        # Display predictions
        if regularity_pred[0] == 1:
            st.success("Cycle Regularity: It is regular.")
        else:
            st.warning("Cycle Regularity: It is irregular. Consult a doctor.")

        st.success(f"Ovulation Date: {ovulation_date.strftime('%Y-%m-%d')}")
        st.success(f"Next Cycle Date: {next_cycle_date.strftime('%Y-%m-%d')}")

        # Provide recommendations based on symptoms
        st.write("Recommendations:")
        if "Cramps" in symptoms:
            st.write("- **Cramps:** Drink herbal teas like chamomile or ginger. Use a heating pad and practice yoga poses like Child’s Pose.")
        if "Fatigue" in symptoms:
            st.write("- **Fatigue:** Get adequate sleep and eat iron-rich foods like spinach and lentils.")
        if "Vomiting/Nausea" in symptoms:
            st.write("- **Vomiting/Nausea:** Sip on ginger tea and avoid greasy or spicy foods.")
        if "Headache" in symptoms:
            st.write("- **Headache:** Stay hydrated and apply a cold compress to your forehead.")
        if "Mood Swings" in symptoms:
            st.write("- **Mood Swings:** Practice mindfulness and eat omega-3-rich foods like salmon.")
        if "Bloating" in symptoms:
            st.write("- **Bloating:** Avoid salty foods and drink peppermint tea.")
        if "Back Pain" in symptoms:
            st.write("- **Back Pain:** Apply a heating pad and practice gentle yoga poses.")
        if "Breast Tenderness" in symptoms:
            st.write("- **Breast Tenderness:** Wear a supportive bra and reduce caffeine intake.")
        if "Food Cravings" in symptoms:
            st.write("- **Food Cravings:** Opt for healthy snacks like fruits and nuts.")
        if "Insomnia" in symptoms:
            st.write("- **Insomnia:** Establish a bedtime routine and avoid screens before bed.")

# Mental Well-being Page
elif page == "Mental Well-being":
    st.title("🧠 Mental Well-being Predictor")
    st.write("Enter your details to assess your mental well-being.")

    # Input fields
    age = st.number_input("Age", min_value=10, max_value=100, value=30)
    family_history = st.selectbox("Do you have a family history of mental health issues?", ["No", "Yes"])
    work_interfere = st.selectbox("Does work interfere with your mental health?", ["Never", "Rarely", "Sometimes", "Often"])
    benefits = st.selectbox("Do you have mental health benefits?", ["No", "Yes"])
    seek_help = st.selectbox("Do you seek help for mental health?", ["No", "Yes"])
    anonymity = st.selectbox("Is anonymity protected in your mental health programs?", ["No", "Yes"])
    mental_health_consequence = st.selectbox("Does discussing mental health have consequences at work?", ["No", "Yes"])

    # Encode inputs
    family_history_yes = 1 if family_history == "Yes" else 0
    work_interfere_often = 1 if work_interfere == "Often" else 0
    work_interfere_rarely = 1 if work_interfere == "Rarely" else 0
    work_interfere_sometimes = 1 if work_interfere == "Sometimes" else 0
    benefits_no = 1 if benefits == "No" else 0
    benefits_yes = 1 if benefits == "Yes" else 0
    seek_help_no = 1 if seek_help == "No" else 0
    seek_help_yes = 1 if seek_help == "Yes" else 0
    anonymity_no = 1 if anonymity == "No" else 0
    anonymity_yes = 1 if anonymity == "Yes" else 0
    mental_health_consequence_no = 1 if mental_health_consequence == "No" else 0
    mental_health_consequence_yes = 1 if mental_health_consequence == "Yes" else 0

    # Prepare input data
    input_data = pd.DataFrame({
        'Age': [age],
        'family_history_Yes': [family_history_yes],
        'work_interfere_Often': [work_interfere_often],
        'work_interfere_Rarely': [work_interfere_rarely],
        'work_interfere_Sometimes': [work_interfere_sometimes],
        'benefits_No': [benefits_no],
        'benefits_Yes': [benefits_yes],
        'seek_help_No': [seek_help_no],
        'seek_help_Yes': [seek_help_yes],
        'anonymity_No': [anonymity_no],
        'anonymity_Yes': [anonymity_yes],
        'mental_health_consequence_No': [mental_health_consequence_no],
        'mental_health_consequence_Yes': [mental_health_consequence_yes]
    })

    # Predict button
    if st.button("Predict"):
        prediction = mental_health_model.predict(input_data)
        st.success(f"Prediction: {prediction[0]}")

        # Provide recommendations based on prediction
        if prediction[0] == "Yes":
            st.warning("Recommendations to Improve Mental Health:")
            st.write("- **Practice Mindfulness:** Engage in meditation or deep breathing exercises.")
            st.write("- **Stay Active:** Regular physical activity can improve mood and reduce stress.")
            st.write("- **Seek Professional Help:** Consider visiting a therapist or counselor for support.")
            st.write("- **Connect with Others:** Share your feelings with trusted friends or family members.")
            st.write("- **Maintain a Healthy Lifestyle:** Eat nutritious meals, sleep well, and avoid excessive caffeine or alcohol.")
        else:
            st.success("Positive Affirmation:")
            st.write("- You are doing great! Keep up the good work and continue taking care of your mental health.")
            st.write("- Remember to practice self-care and stay connected with loved ones.")