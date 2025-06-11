import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Pima Diabetes Predictor",
    layout="centered"
)

# --- API URL ---
API_URL = "https://pimapy-api.onrender.com/predict"


# --- App Title ---
st.title("Pima Diabetes Predictor")


# --- Input Form ---
with st.form(key="prediction_form"):
    st.write("Please enter the patient's details below.")
    
    col1, col2 = st.columns(2)

    with col1:
        # The variable names here can be anything, the 'payload' mapping is what matters.
        in_pregnant = st.number_input("Pregnant (0-17)", 0, 17, 6, 1)
        in_blood_pr = st.number_input("Blood Pressure (0-122 mmHg)", 0.0, 122.0, 72.0, 0.1, "%.1f")
        in_insulin = st.number_input("Insulin (0-846 µU/mL)", 0.0, 846.0, 0.0, 0.1, "%.1f")
        in_dbts_pdgr = st.number_input("Diabetes Pedigree (0.078-2.42)", 0.078, 2.420, 0.627, 0.001, "%.3f")

    with col2:
        in_glucose = st.number_input("Glucose (0-199 mg/dL)", 0.0, 199.0, 148.0, 0.1, "%.1f")
        in_skin_thi = st.number_input("Skin Thickness (0-99 mm)", 0.0, 99.0, 35.0, 0.1, "%.1f")
        in_bmi = st.number_input("BMI (0-67.1)", 0.0, 67.1, 33.6, 0.1, "%.1f")
        in_age = st.number_input("Age (21-81 years)", 21, 81, 50, 1)

    submit_button = st.form_submit_button(label="Get Prediction", use_container_width=True)


# --- Prediction Logic ---
if submit_button:
    # --- THIS IS THE FIX ---
    # The keys in this dictionary now match the API's 'ModelInput' schema exactly.
    payload = {
        "pregnant": in_pregnant,
        "glucose": in_glucose,
        "blood_pr": in_blood_pr,
        "skin_thi": in_skin_thi,
        "insulin": in_insulin,
        "bmi": in_bmi,
        "dbts_pdgr": in_dbts_pdgr,
        "age": in_age,
    }

    with st.spinner("Predicting..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            prediction = data.get("prediction", "N/A")
            probability = data.get("probability_diabetic", "N/A")
            
            if prediction.lower() == "non-diabetic":
                st.success(f"**Prediction: {prediction}** (Probability: {probability})")
            else:
                st.warning(f"**Prediction: {prediction}** (Probability: {probability})")

        except requests.exceptions.HTTPError as e:
            # This will now correctly show the validation error detail from FastAPI
            st.error(f"Prediction failed: {e.response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
