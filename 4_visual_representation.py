
from pathlib import Path
from theme import apply_light_theme

import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Visual Representation",
    page_icon="📊",
    layout="wide"
)
apply_light_theme()
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "adult_income_processed.csv"

st.title("📊 Visual Representation")
st.write(
    "Explore the income dataset through interactive charts "
    "and visual summaries."
)

# Load the dataset
if not DATA_PATH.exists():
    st.error("Dataset file not found!")
    st.code(str(DATA_PATH))
    st.info(
        "Check that adult_income_processed.csv is inside "
        "the data folder in your project."
    )
    st.stop()

try:
    data = pd.read_csv(DATA_PATH)
except Exception as error:
    st.error(f"Could not read the dataset: {error}")
    st.stop()

if data.empty:
    st.error("Your dataset is empty.")
    st.stop()

# Clean column names
data.columns = data.columns.astype(str).str.strip()

st.success("Dataset loaded successfully!")

# Dataset overview
st.subheader("1. Dataset Overview")

a, b, c = st.columns(3)
a.metric("Total Records", f"{len(data):,}")
b.metric("Total Columns", len(data.columns))
c.metric("Missing Values", f"{data.isna().sum().sum():,}")

with st.expander("Check dataset columns"):
    st.write(data.columns.tolist())
    st.dataframe(data.head(10), use_container_width=True)

st.divider()

# Find the income target column
target_candidates = [
    "income_category",
    "income",
    "class",
    "target"
]

target = next(
    (
        col for col in data.columns
        if col.lower().strip() in target_candidates
    ),
    None
)

# Income distribution graph
st.subheader("2. Income Category Distribution")

if target is not None:
    income_counts = (
        data[target]
        .fillna("Missing")
        .astype(str)
        .value_counts()
        .rename_axis("Income Category")
        .reset_index(name="Records")
    )

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            income_counts,
            x="Income Category",
            y="Records",
            color="Income Category",
            text="Records",
            title="Records in Each Income Category",
            template="plotly_white"
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(
            fig, use_container_width=True,
            key="income_bar"
        )

    with right:
        fig = px.pie(
            income_counts,
            names="Income Category",
            values="Records",
            hole=0.4,
            title="Income Category Proportions",
            template="plotly_white"
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(
            fig, use_container_width=True,
            key="income_pie"
        )

else:
    st.warning(
        "Could not identify the income target column automatically. "
        "Choose the correct column below."
    )

    chosen_target = st.selectbox(
        "Select your income category column",
        options=data.columns.tolist()
    )

    income_counts = (
        data[chosen_target]
        .fillna("Missing")
        .astype(str)
        .value_counts()
        .rename_axis("Income Category")
        .reset_index(name="Records")
    )

    fig = px.bar(
        income_counts,
        x="Income Category",
        y="Records",
        color="Income Category",
        title="Distribution of Selected Column",
        template="plotly_white"
    )
    st.plotly_chart(
        fig, use_container_width=True,
        key="selected_column_chart"
    )

st.divider()

# Numeric feature visualization
st.subheader("3. Numeric Feature Analysis")

numeric_columns = data.select_dtypes(
    include="number"
).columns.tolist()

if numeric_columns:
    feature = st.selectbox(
        "Choose a numeric feature",
        numeric_columns
    )

    feature_data = data[feature].dropna()

    if not feature_data.empty:
        chart_data = pd.DataFrame({
            "Value": feature_data
        })

        fig = px.histogram(
            chart_data,
            x="Value",
            nbins=30,
            title=f"Distribution of {feature}",
            labels={"Value": feature},
            template="plotly_white"
        )

        st.plotly_chart(
            fig, use_container_width=True,
            key="numeric_histogram"
        )

        st.write("Summary statistics")
        st.dataframe(
            feature_data.describe().to_frame(
                name="Statistics"
            ).round(2),
            use_container_width=True
        )
    else:
        st.info("No valid numeric values for this feature.")
else:
    st.info(
        "No numeric columns were detected. "
        "Check whether the dataset contains encoded numeric features."
    )

st.divider()

# Categorical feature visualization
st.subheader("4. Feature Comparison")

categorical_columns = [
    col for col in data.select_dtypes(
        include=["object", "category", "bool"]
    ).columns
    if col != target
    and data[col].nunique(dropna=True) > 1
]

if categorical_columns:
    feature = st.selectbox(
        "Choose a categorical feature",
        categorical_columns,
        key="categorical_feature"
    )

    plot_data = data[[feature]].copy()
    plot_data[feature] = (
        plot_data[feature].fillna("Missing").astype(str)
    )

    top_values = plot_data[feature].value_counts().head(15).index
    plot_data = plot_data[plot_data[feature].isin(top_values)]

    counts = (
        plot_data[feature]
        .value_counts()
        .rename_axis(feature)
        .reset_index(name="Records")
    )

    fig = px.bar(
        counts,
        x=feature,
        y="Records",
        color=feature,
        title=f"Records by {feature}",
        template="plotly_white"
    )
    fig.update_layout(showlegend=False, xaxis_tickangle=-30)

    st.plotly_chart(
        fig, use_container_width=True,
        key="categorical_chart"
    )
else:
    st.info(
        "No text-based categorical features were found. "
        "Your preprocessing may have encoded them as numbers."
    )

st.divider()

st.caption(
    "Educational use only. These charts describe the supplied "
    "dataset and do not establish causation or guarantee real-world "
    "income outcomes."
)
