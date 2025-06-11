import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Pima Diabetes Predictor",
    layout="centered"
)

# --- API URL ---
# This should point to your live Render deployment
API_URL = "https://pimapy-api.onrender.com/predict"


# --- App Title ---
st.title("Pima Diabetes Predictor")


# --- Input Form ---
# Using a form prevents the app from re-running on every input change.
with st.form(key="prediction_form"):
    st.write("Please enter the patient's details below.")
    
    col1, col2 = st.columns(2)

    with col1:
        # These variable names can be anything, but we will map them to the correct
        # API names in the payload dictionary.
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=17, value=6, step=1)
        blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=0.0, max_value=122.0, value=72.0, step=0.1, format="%.1f")
        insulin = st.number_input("Insulin (µU/mL)", min_value=0.0, max_value=846.0, value=0.0, step=0.1, format="%.1f")
        diabetes_pedigree = st.number_input("Diabetes Pedigree Function", min_value=0.078, max_value=2.420, value=0.627, step=0.001, format="%.3f")

    with col2:
        glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=199.0, value=148.0, step=0.1, format="%.1f")
        skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0.0, max_value=99.0, value=35.0, step=0.1, format="%.1f")
        bmi = st.number_input("BMI", min_value=0.0, max_value=67.1, value=33.6, step=0.1, format="%.1f")
        age = st.number_input("Age (years)", min_value=21, max_value=81, value=50, step=1)

    # The submit button for the form
    submit_button = st.form_submit_button(label="Get Prediction", use_container_width=True)


# --- Prediction Logic ---
if submit_button:
    # --- FIX 1: Correct the payload keys ---
    # The keys in this dictionary MUST match the Pydantic 'ModelInput' schema in your FastAPI app.
    payload = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": diabetes_pedigree,
        "Age": age,
    }

    with st.spinner("Predicting..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=20) # Increased timeout for cold starts
            response.raise_for_status()

            data = response.json()
            
            # --- FIX 2: Correct the response key ---
            # Get the prediction and the probability using the correct keys from the API response.
            prediction = data.get("prediction", "N/A")
            probability = data.get("probability_diabetic", "N/A") # Changed from "probability"
            
            if prediction.lower() == "non-diabetic":
                st.success(f"**Prediction: {prediction}** (Probability: {probability})")
            else:
                st.warning(f"**Prediction: {prediction}** (Probability: {probability})")

        except requests.exceptions.HTTPError as e:
            # Handle specific API errors, showing the detail from the response
            st.error(f"Prediction failed: {e.response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

