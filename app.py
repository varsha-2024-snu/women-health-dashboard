# Import libraries
import streamlit as st
import joblib
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Load models
maternal_health_model = joblib.load('maternal_health_model.pkl')
model_regularity = joblib.load('model_regularity (1).pkl')
model_ovulation = joblib.load('model_ovulation (1).pkl')
mental_health_model = joblib.load('women_mental_health_model.pkl')

# Load datasets
maternal_health_data = pd.read_csv('Maternal Health Risk Data Set.csv')
menstrual_cycle_data = pd.read_csv('Menstural_cyclelength.csv')
mental_health_survey_data = pd.read_csv('survey.csv')

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
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #ec628b !important;
        padding-top: 20px !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] * {
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        font-family: 'Arial', sans-serif !important;
    }

    /* Customize radio button (navigation menu) */
    div[data-testid="stSidebar"] div[role="radiogroup"] label {
        display: flex;
        align-items: center;
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        transition: background-color 0.3s ease;
    }

    /* Change color of selected radio button */
    div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.4);
    }

    /* Highlight the selected item */
    div[data-testid="stSidebar"] div[aria-checked="true"] {
        background-color: white !important;
        color: #ec628b !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }

    /* Remove default radio button circle */
    div[data-testid="stSidebar"] div[role="radiogroup"] label span {
        display: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Set up the sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Maternal Health", "Menstrual Cycle", "Mental Well-being", "BMI Calculator", "Hydration Tracker"])

# Home Page
if page == "Home":
    st.title("🌸 Women's Health Dashboard 🌸")
    st.write("Welcome to the Women's Health Dashboard! Use the sidebar to navigate to different sections.")
    
    # Add an image
    st.image("image1.jpg", caption="Empowering Women Through Health Awareness", use_container_width=True)

    # Data Analytics Section
    st.header("📊 Data Analytics for Women's Health Awareness")

    # Maternal Health Analytics
    st.subheader("1. Maternal Health Risk Analysis")
    st.write("How each factor contributes to high-risk maternal health:")

    # Filter high-risk cases
    high_risk_data = maternal_health_data[maternal_health_data['RiskLevel'] == 'high risk']

    # Plotting
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=high_risk_data[['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']], ax=ax1, palette='viridis')
    ax1.set_title("Distribution of Factors Contributing to High-Risk Maternal Health")
    ax1.set_ylabel("Value")
    st.pyplot(fig1)
    st.write("This graph shows the distribution of factors like age, blood pressure, blood sugar, body temperature, and heart rate for high-risk maternal health cases.")

    # Menstrual Health Analytics
    st.subheader("2. Menstrual Health Analysis")
    st.write("Distribution of Menstrual Cycle Lengths:")

    # Check if 'cycle_length' column exists
    if 'cycle_length' in menstrual_cycle_data.columns:
        # Histogram for Cycle Lengths
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.histplot(menstrual_cycle_data['cycle_length'], bins=20, kde=True, color='purple', ax=ax2)
        ax2.set_title("Distribution of Menstrual Cycle Lengths")
        ax2.set_xlabel("Cycle Length (Days)")
        ax2.set_ylabel("Frequency")
        st.pyplot(fig2)
        st.write("This graph shows the distribution of menstrual cycle lengths among women.")
    else:
        st.warning("The dataset does not contain the 'cycle_length' column. Displaying available columns:")
        st.write(menstrual_cycle_data.columns)

        # If 'cycle_length' is not available, display any other relevant graph
        if len(menstrual_cycle_data.columns) > 0:
            # Plot the first numeric column as an example
            numeric_columns = menstrual_cycle_data.select_dtypes(include=['int', 'float']).columns
            if len(numeric_columns) > 0:
                column_to_plot = numeric_columns[0]
                fig2, ax2 = plt.subplots(figsize=(10, 6))
                sns.histplot(menstrual_cycle_data[column_to_plot], bins=20, kde=True, color='purple', ax=ax2)
                ax2.set_title(f"Distribution of {column_to_plot}")
                ax2.set_xlabel(column_to_plot)
                ax2.set_ylabel("Frequency")
                st.pyplot(fig2)
                st.write(f"This graph shows the distribution of {column_to_plot}.")
            else:
                st.warning("No numeric columns found in the dataset for visualization.")
        else:
            st.warning("The dataset is empty or contains no columns.")

    # Mental Health Analytics
    st.subheader("3. Mental Health Analysis")
    st.write("Number of women affected by mental health diseases:")

    # Filter data for women
    women_mental_health_data = mental_health_survey_data[mental_health_survey_data['Gender'] == 'Female']
    if 'treatment' in women_mental_health_data.columns:
        fig3, ax3 = plt.subplots()
        sns.countplot(x='treatment', data=women_mental_health_data, palette='coolwarm', ax=ax3)
        ax3.set_title("Women Seeking Mental Health Treatment")
        ax3.set_xlabel("Sought Treatment")
        ax3.set_ylabel("Count")
        st.pyplot(fig3)
        st.write("This graph shows the number of women who sought mental health treatment versus those who did not.")
    else:
        st.warning("The 'treatment' column is not present in the dataset.")

# Maternal Health Page
elif page == "Maternal Health":
    st.title("🤰 Maternal Health Predictor")
    st.write("Enter your details to predict maternal health risks.")

    # Input fields
    age = st.number_input("Age", min_value=10, max_value=50, value=25)
    systolic_bp = st.number_input("Systolic Blood Pressure", min_value=50, max_value=200, value=120)
    diastolic_bp = st.number_input("Diastolic Blood Pressure", min_value=30, max_value=150, value=80)
    bs = st.number_input("Blood Sugar Level", min_value=2.0, max_value=20.0, value=5.0)
    body_temp = st.number_input("Body Temperature", min_value=80.0, max_value=120.0, value=98.0)
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

# BMI Calculator Page
# BMI Calculator Page
elif page == "BMI Calculator":
    st.title("📊 BMI Calculator")
    st.write("Calculate your Body Mass Index (BMI) and get personalized recommendations.")

    # Input fields for height and weight
    height_unit = st.radio("Select height unit:", ["Centimeters (cm)", "Meters (m)"])
    if height_unit == "Centimeters (cm)":
        height = st.number_input("Enter your height (in cm):", min_value=50, max_value=250, value=160)
        height_m = height / 100  # Convert cm to meters
    else:
        height_m = st.number_input("Enter your height (in meters):", min_value=1.0, max_value=2.5, value=1.6)

    weight_unit = st.radio("Select weight unit:", ["Kilograms (kg)", "Pounds (lbs)"])
    if weight_unit == "Kilograms (kg)":
        weight = st.number_input("Enter your weight (in kg):", min_value=30, max_value=300, value=60)
    else:
        weight_lbs = st.number_input("Enter your weight (in lbs):", min_value=66, max_value=660, value=132)
        weight = weight_lbs * 0.453592  # Convert lbs to kg

    # Calculate BMI
    if st.button("Calculate BMI"):
        if height_m <= 0 or weight <= 0:
            st.error("Please enter valid height and weight values.")
        else:
            bmi = weight / (height_m ** 2)
            st.success(f"Your BMI is: **{bmi:.2f}**")

            # BMI Categories and Recommendations
            if bmi < 18.5:
                st.warning("**Category:** Underweight")
                st.write("**Recommendations:**")
                st.write("- Focus on gaining weight through a balanced diet rich in proteins, healthy fats, and carbohydrates.")
                st.write("- Include strength training exercises to build muscle mass.")
                st.write("- Consult a nutritionist for a personalized diet plan.")
            elif 18.5 <= bmi < 24.9:
                st.success("**Category:** Normal Weight")
                st.write("**Recommendations:**")
                st.write("- Maintain a healthy lifestyle with regular exercise and a balanced diet.")
                st.write("- Stay hydrated and avoid excessive junk food.")
                st.write("- Regular health check-ups are recommended.")
            elif 25 <= bmi < 29.9:
                st.warning("**Category:** Overweight")
                st.write("**Recommendations:**")
                st.write("- Focus on losing weight through a calorie deficit diet and regular exercise.")
                st.write("- Include more fruits, vegetables, and whole grains in your diet.")
                st.write("- Avoid sugary drinks and processed foods.")
            else:
                st.error("**Category:** Obese")
                st.write("**Recommendations:**")
                st.write("- Seek professional help from a doctor or nutritionist for weight management.")
                st.write("- Incorporate daily physical activity like walking, jogging, or yoga.")
                st.write("- Avoid high-calorie foods and focus on portion control.")

    # Additional Tips
    st.markdown("### 🍎 Healthy Eating Tips")
    st.write("- Eat a variety of fruits and vegetables daily.")
    st.write("- Choose whole grains over refined grains.")
    st.write("- Limit your intake of added sugars and saturated fats.")
    st.write("- Stay hydrated by drinking plenty of water.")

    st.markdown("### 🏋️‍♀️ Exercise Tips")
    st.write("- Aim for at least 30 minutes of moderate exercise daily.")
    st.write("- Include strength training exercises twice a week.")
    st.write("- Try activities like yoga, swimming, or cycling for variety.")

    # Hydration Tracker Page
elif page == "Hydration Tracker":
    st.title("💧 Hydration Tracker")
    st.write("Track your daily water intake and stay hydrated!")

    # Daily Water Intake Recommendation
    st.markdown("### 🚰 Daily Water Intake Recommendation")
    weight_kg = st.number_input("Enter your weight (in kg):", min_value=30, max_value=300, value=60)
    activity_level = st.selectbox("Select your activity level:", ["Sedentary", "Moderately Active", "Very Active"])
    
    # Calculate recommended water intake
    if activity_level == "Sedentary":
        water_intake_ml = weight_kg * 30  # 30 ml per kg of body weight
    elif activity_level == "Moderately Active":
        water_intake_ml = weight_kg * 35  # 35 ml per kg of body weight
    else:
        water_intake_ml = weight_kg * 40  # 40 ml per kg of body weight

    st.success(f"Your recommended daily water intake is **{water_intake_ml:.0f} ml**.")

    # Water Intake Tracker
    st.markdown("### 📊 Track Your Water Intake")
    st.write("Log how much water you've consumed today:")

    # Input for water intake
    water_consumed_ml = st.number_input("Enter the amount of water consumed (in ml):", min_value=0, max_value=5000, value=0)

    # Calculate remaining water intake
    remaining_water_ml = max(0, water_intake_ml - water_consumed_ml)
    st.write(f"Remaining water to drink today: **{remaining_water_ml:.0f} ml**.")

    # Progress Bar
    progress = min(1.0, water_consumed_ml / water_intake_ml)
    st.progress(progress)
    st.write(f"You've consumed **{progress * 100:.1f}%** of your daily goal.")

    # Hydration Tips
    st.markdown("### 💡 Hydration Tips")
    st.write("- Start your day with a glass of water.")
    st.write("- Carry a reusable water bottle with you.")
    st.write("- Set reminders to drink water throughout the day.")
    st.write("- Eat water-rich foods like cucumbers, watermelon, and oranges.")
    st.write("- Avoid sugary drinks and opt for water instead.")

    # Reminder Feature
    st.markdown("### ⏰ Set a Hydration Reminder")
    reminder_frequency = st.selectbox("How often would you like to be reminded to drink water?", ["Every 30 minutes", "Every 1 hour", "Every 2 hours"])
    
    if st.button("Set Reminder"):
        if reminder_frequency == "Every 30 minutes":
            st.write("🔔 Reminder set: Drink water every 30 minutes!")
        elif reminder_frequency == "Every 1 hour":
            st.write("🔔 Reminder set: Drink water every 1 hour!")
        else:
            st.write("🔔 Reminder set: Drink water every 2 hours!")
        st.write("Stay consistent and keep hydrating! 💧")
