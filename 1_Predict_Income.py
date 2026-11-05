from theme import apply_light_theme
from pathlib import Path


import joblib
import pandas as pd
import streamlit as st



# ----------------------------------
# 1. PROJECT PATHS
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"
CSS_PATH = BASE_DIR / "assets" / "style.css"


# ----------------------------------
# 2. PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Predict Income | IncomeAI",
    page_icon="🔮",
    layout="wide"
)
apply_light_theme()


# ----------------------------------
# 3. LOAD CUSTOM CSS
# ----------------------------------

if CSS_PATH.exists():
    with open(CSS_PATH, encoding="utf-8") as file:
        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )


# ----------------------------------
# 4. PAGE HEADER
# ----------------------------------

st.title("🔮 Employee Income Prediction")

st.write(
    "Enter employee information below to predict "
    "the income category using machine learning."
)

st.info(
    "This project uses Logistic Regression, Decision Tree "
    "and Linear SVM algorithms."
)


# ----------------------------------
# 5. LOAD TRAINED MODEL
# ----------------------------------

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


if not MODEL_PATH.exists():
    st.error("Trained model not found. Please run train_model.py first.")
    st.stop()

model = load_model()


# ----------------------------------
# 6. EMPLOYEE DETAILS FORM
# ----------------------------------

st.subheader("Employee Information")

with st.form("income_prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### Personal Information")

        age = st.number_input(
            "Age",
            min_value=17,
            max_value=100,
            value=30
        )

        sex = st.selectbox(
            "Sex",
            ["Male", "Female"]
        )

        race = st.selectbox(
            "Race",
            [
                "White",
                "Black",
                "Asian-Pac-Islander",
                "Amer-Indian-Eskimo",
                "Other"
            ]
        )

        native_country = st.selectbox(
            "Native Country",
            [
                "United-States",
                "India",
                "Canada",
                "Germany",
                "England",
                "Mexico",
                "Philippines",
                "China",
                "Japan",
                "Italy",
                "Other"
            ]
        )

        st.markdown("#### Education Details")

        education = st.selectbox(
            "Education",
            [
                "Bachelors",
                "Some-college",
                "11th",
                "HS-grad",
                "Prof-school",
                "Assoc-acdm",
                "Assoc-voc",
                "9th",
                "7th-8th",
                "12th",
                "Masters",
                "1st-4th",
                "10th",
                "Doctorate",
                "5th-6th",
                "Preschool"
            ]
        )

        education_num = st.number_input(
            "Education Number",
            min_value=1,
            max_value=16,
            value=10
        )

    with col2:

        st.markdown("#### Employment Information")

        workclass = st.selectbox(
            "Work Class",
            [
                "Private",
                "Self-emp-not-inc",
                "Self-emp-inc",
                "Federal-gov",
                "Local-gov",
                "State-gov",
                "Without-pay",
                "Never-worked"
            ]
        )

        occupation = st.selectbox(
            "Occupation",
            [
                "Tech-support",
                "Craft-repair",
                "Other-service",
                "Sales",
                "Exec-managerial",
                "Prof-specialty",
                "Handlers-cleaners",
                "Machine-op-inspct",
                "Adm-clerical",
                "Farming-fishing",
                "Transport-moving",
                "Priv-house-serv",
                "Protective-serv",
                "Armed-Forces"
            ]
        )

        marital_status = st.selectbox(
            "Marital Status",
            [
                "Married-civ-spouse",
                "Divorced",
                "Never-married",
                "Separated",
                "Widowed",
                "Married-spouse-absent",
                "Married-AF-spouse"
            ]
        )

        relationship = st.selectbox(
            "Relationship",
            [
                "Wife",
                "Own-child",
                "Husband",
                "Not-in-family",
                "Other-relative",
                "Unmarried"
            ]
        )

        fnlwgt = st.number_input(
            "Final Weight",
            min_value=1,
            value=200000
        )

        st.markdown("#### Financial Information")

        capital_gain = st.number_input(
            "Capital Gain",
            min_value=0,
            value=0
        )

        capital_loss = st.number_input(
            "Capital Loss",
            min_value=0,
            value=0
        )

        hours_per_week = st.number_input(
            "Hours Worked Per Week",
            min_value=1,
            max_value=99,
            value=40
        )

    submitted = st.form_submit_button(
        "🔍 Predict Income",
        use_container_width=True
    )


# ----------------------------------
# 7. MAKE INCOME PREDICTION
# ----------------------------------

if submitted:

    employee_data = pd.DataFrame([{
        "age": age,
        "workclass": workclass,
        "fnlwgt": fnlwgt,
        "education": education,
        "education-num": education_num,
        "marital-status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "sex": sex,
        "capital-gain": capital_gain,
        "capital-loss": capital_loss,
        "hours-per-week": hours_per_week,
        "native-country": native_country
    }])

    try:

        prediction = model.predict(employee_data)[0]

        st.divider()

        st.subheader("Prediction Result")

        if prediction == ">50K":

            st.success(
                "Predicted Income Category: ABOVE $50K"
            )

            st.markdown(
                "The model predicts that this record belongs "
                "to the income category above $50K."
            )

        else:

            st.info(
                "Predicted Income Category: $50K OR BELOW"
            )

            st.markdown(
                "The model predicts that this record belongs "
                "to the income category of $50K or below."
            )

        st.caption(
            "Note: This is an educational machine-learning "
            "prediction based on historical census data. "
            "It is not a guarantee of actual individual income."
        )

    except Exception as error:

        st.error("Unable to generate prediction.")

        st.code(str(error))


# ----------------------------------
# 8. FOOTER
# ----------------------------------

st.divider()

st.caption(
    "Employee Income Category Predictor | "
    "Machine Learning Internship Project"
)

# ===== LIGHT THEME OVERRIDE =====
st.markdown("""
<style>
/* Main page background */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section[data-testid="stMain"] {
    background: #F4F7FB !important;
    background-image: none !important;
    color: #243247 !important;
}

/* Remove dark gradient overlays */
[data-testid="stAppViewContainer"]::before,
[data-testid="stAppViewContainer"]::after,
.stApp::before,
.stApp::after {
    background: none !important;
    background-image: none !important;
    opacity: 0 !important;
}

/* Main content */
.block-container {
    background: transparent !important;
}

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
}

/* Headings */
h1, h2, h3, h4 {
    color: #1E3A5F !important;
}

/* Text and field labels */
p, label,
[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"] {
    color: #334155 !important;
}

/* Form sections and custom cards */
div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stForm"],
div[data-testid="stExpander"] {
    background: #FFFFFF !important;
    background-image: none !important;
    border-color: #E2E8F0 !important;
    border-radius: 14px !important;
}

/* Input boxes */
.stNumberInput input,
.stTextInput input,
.stTextArea textarea,
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #243247 !important;
    border-color: #CBD5E1 !important;
    border-radius: 8px !important;
}

/* Buttons */
.stButton > button {
    background: #DBEAFE !important;
    background-image: none !important;
    color: #1D4ED8 !important;
    border: 1px solid #BFDBFE !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* Prediction result panels */
div[data-testid="stAlert"] {
    background: #E8F5E9 !important;
    color: #166534 !important;
    border-radius: 12px !important;
}

/* Dividers */
hr {
    border-color: #E2E8F0 !important;
}
</style>
""", unsafe_allow_html=True)
