from pathlib import Path
from theme import apply_light_theme

import pandas as pd
import plotly.express as px
import streamlit as st


# ----------------------------------
# 1. PROJECT PATHS
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_PATH = BASE_DIR / "models" / "model_comparison.csv"
CSS_PATH = BASE_DIR / "assets" / "style.css"


# ----------------------------------
# 2. PAGE SETTINGS AND CSS
# ----------------------------------

st.set_page_config(
    page_title="Model Comparison | IncomeAI",
    page_icon="📊",
    layout="wide"
)
apply_light_theme()

if CSS_PATH.exists():
    with open(CSS_PATH, encoding="utf-8") as file:
        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )


# ----------------------------------
# 3. PAGE HEADING
# ----------------------------------

st.title("📊 Model Performance Comparison")

st.write(
    "Compare the performance of Logistic Regression, "
    "Decision Tree, and Linear SVM."
)


# ----------------------------------
# 4. LOAD MODEL RESULTS
# ----------------------------------

if not RESULTS_PATH.exists():
    st.error("Model comparison results not found.")
    st.info("Please run train_model.py first.")
    st.stop()

results = pd.read_csv(RESULTS_PATH)

if results.empty:
    st.warning("No model results are available.")
    st.stop()


# ----------------------------------
# 5. DISPLAY BEST MODEL
# ----------------------------------

best_model = results.iloc[0]

st.subheader("Best Performing Model")

st.success(
    f"{best_model['Model']} achieved the highest F1 Score "
    f"({best_model['F1 Score']:.4f})."
)


# ----------------------------------
# 6. PERFORMANCE METRICS
# ----------------------------------

st.subheader("Performance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Best Accuracy",
    f"{results['Accuracy'].max():.2%}"
)

col2.metric(
    "Best Precision",
    f"{results['Precision'].max():.2%}"
)

col3.metric(
    "Best Recall",
    f"{results['Recall'].max():.2%}"
)

col4.metric(
    "Best F1 Score",
    f"{results['F1 Score'].max():.2%}"
)


# ----------------------------------
# 7. MODEL COMPARISON TABLE
# ----------------------------------

st.subheader("Detailed Model Results")

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True
)


# ----------------------------------
# 8. PERFORMANCE CHART
# ----------------------------------

st.subheader("Model Performance Chart")

metric = st.selectbox(
    "Choose a performance metric",
    ["Accuracy", "Precision", "Recall", "F1 Score"]
)

fig = px.bar(
    results,
    x="Model",
    y=metric,
    color="Model",
    text=metric,
    title=f"Comparison of Models by {metric}",
    range_y=[0, 1]
)

fig.update_traces(
    texttemplate="%{text:.2%}",
    textposition="outside"
)

fig.update_layout(
    yaxis_title=metric,
    xaxis_title="Machine Learning Model",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ----------------------------------
# 9. TRAINING TIME CHART
# ----------------------------------

st.subheader("Training Time Comparison")

time_fig = px.bar(
    results,
    x="Model",
    y="Training Time (seconds)",
    color="Model",
    text="Training Time (seconds)",
    title="Training Time for Each Model"
)

time_fig.update_layout(
    xaxis_title="Machine Learning Model",
    yaxis_title="Training Time (seconds)",
    showlegend=False
)

st.plotly_chart(
    time_fig,
    use_container_width=True
)


# ----------------------------------
# 10. EXPLANATION OF METRICS
# ----------------------------------

st.subheader("Understanding the Evaluation Metrics")

with st.expander("What do these metrics mean?"):

    st.markdown("""
    **Accuracy:** The percentage of all predictions
    that were correct.

    **Precision:** Of the records predicted as above $50K,
    how many actually belonged to that category?

    **Recall:** Of all records actually above $50K,
    how many did the model correctly identify?

    **F1 Score:** A combined measure of precision and recall.

    **Training Time:** The time taken by the model
    to complete training.
    """)

st.caption(
    "The models are ranked by F1 Score. "
    "Results are based on the project's held-out test dataset."
)