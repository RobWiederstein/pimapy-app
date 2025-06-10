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
# Using a form prevents the app from re-running on every input change.
# The API call will only be made when the button inside the form is clicked.
with st.form(key="prediction_form"):
    st.write("Please enter the patient's details below.")
    
    # Create two columns for the input fields
    col1, col2 = st.columns(2)

    with col1:
        pregnant = st.number_input("Pregnant (0-17)", min_value=0, max_value=17, value=6, step=1)
        blood_pr = st.number_input("Blood Pressure (0-122 mmHg)", min_value=0.0, max_value=122.0, value=72.0, step=0.1, format="%.1f")
        insulin = st.number_input("Insulin (0-846 µU/mL)", min_value=0.0, max_value=846.0, value=0.0, step=0.1, format="%.1f")
        dbts_pdgr = st.number_input("Diabetes Pedigree (0.078-2.42)", min_value=0.078, max_value=2.420, value=0.627, step=0.001, format="%.3f")

    with col2:
        glucose = st.number_input("Glucose (0-199 mg/dL)", min_value=0.0, max_value=199.0, value=148.0, step=0.1, format="%.1f")
        skin_thi = st.number_input("Skin Thickness (0-99 mm)", min_value=0.0, max_value=99.0, value=35.0, step=0.1, format="%.1f")
        bmi = st.number_input("BMI (0-67.1)", min_value=0.0, max_value=67.1, value=33.6, step=0.1, format="%.1f")
        age = st.number_input("Age (21-81 years)", min_value=21, max_value=81, value=50, step=1)

    # The submit button for the form
    submit_button = st.form_submit_button(label="Get Prediction", use_container_width=True)


# --- Prediction Logic ---
# This block runs only when the submit button is pressed.
if submit_button:
    # Construct the payload for the API
    payload = {
        "pregnant": pregnant,
        "glucose": glucose,
        "blood_pr": blood_pr,
        "skin_thi": skin_thi,
        "insulin": insulin,
        "bmi": bmi,
        "dbts_pdgr": dbts_pdgr,
        "age": age,
        "flag_imp": 0,  # Hard-coded as before
    }

    # Show a spinner while waiting for the API response
    with st.spinner("Predicting..."):
        try:
            # Make the POST request to the API
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()  # Raise an error for bad status codes

            # Process the successful response
            data = response.json()
            prediction = data.get("prediction", "N/A")
            probability = data.get("probability", "N/A")
            
            # Display the result in a colored box
            if prediction.lower() == "non-diabetic":
                st.success(f"**Prediction: {prediction}** (Probability: {probability})")
            else:
                st.warning(f"**Prediction: {prediction}** (Probability: {probability})")

        except requests.exceptions.RequestException as e:
            # Handle network or API errors
            st.error(f"API request failed: {e}")
        except Exception as e:
            # Handle other unexpected errors
            st.error(f"An unexpected error occurred: {e}")

