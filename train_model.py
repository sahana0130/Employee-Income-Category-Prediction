from pathlib import Path
import time

import joblib
import pandas as pd
from ucimlrepo import fetch_ucirepo

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC


# ----------------------------------
# 1. PROJECT PATHS
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

DATA_PATH = DATA_DIR / "adult_income_processed.csv"
MODEL_PATH = MODEL_DIR / "best_model.joblib"
RESULTS_PATH = MODEL_DIR / "model_comparison.csv"


# ----------------------------------
# 2. DOWNLOAD THE DATASET
# ----------------------------------

print("\nDownloading Adult Census Income dataset...")

adult = fetch_ucirepo(id=2)

X = adult.data.features.copy()
y = adult.data.targets.copy()

# Convert target into a single column
if isinstance(y, pd.DataFrame):
    y = y.iloc[:, 0]

# Clean spaces and missing-value symbols
X = X.replace(r"^\s*\?\s*$", pd.NA, regex=True)

for column in X.select_dtypes(include=["object"]).columns:
    X[column] = X[column].str.strip()

# Clean target labels
y = y.astype(str).str.strip().str.replace(".", "", regex=False)

# Convert income labels into two categories
y = y.apply(
    lambda value: ">50K" if value.startswith(">50K") else "<=50K"
)

# Remove rows with missing target values
valid_rows = y.notna()
X = X.loc[valid_rows].reset_index(drop=True)
y = y.loc[valid_rows].reset_index(drop=True)

data = X.copy()
data["income_category"] = y

data.to_csv(DATA_PATH, index=False)

print("Dataset downloaded and saved successfully.")
print("Dataset shape:", data.shape)
print("\nIncome category distribution:")
print(y.value_counts())


# ----------------------------------
# 3. SELECT FEATURES AND TARGET
# ----------------------------------

X = data.drop(columns=["income_category"])
y = data["income_category"]

numeric_columns = X.select_dtypes(
    include=["number"]
).columns.tolist()

categorical_columns = X.select_dtypes(
    exclude=["number"]
).columns.tolist()

print("\nNumerical columns:", len(numeric_columns))
print("Categorical columns:", len(categorical_columns))


# ----------------------------------
# 4. PREPROCESS THE DATA
# ----------------------------------

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_columns),
        ("categorical", categorical_pipeline, categorical_columns)
    ]
)


# ----------------------------------
# 5. SPLIT THE DATA
# ----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ----------------------------------
# 6. DEFINE MACHINE-LEARNING MODELS
# ----------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        class_weight="balanced",
        random_state=42
    ),

    "Linear SVM": LinearSVC(
        class_weight="balanced",
        random_state=42,
        max_iter=5000
    )
}


# ----------------------------------
# 7. TRAIN AND EVALUATE MODELS
# ----------------------------------

results = []
trained_models = {}

print("\nStarting model training...\n")

for model_name, model in models.items():

    print("Training:", model_name)

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", model)
        ]
    )

    start_time = time.time()

    pipeline.fit(X_train, y_train)

    training_time = time.time() - start_time

    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        pos_label=">50K",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        pos_label=">50K",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        pos_label=">50K",
        zero_division=0
    )

    results.append({
        "Model": model_name,
        "Accuracy": round(accuracy, 4),
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1 Score": round(f1, 4),
        "Training Time (seconds)": round(training_time, 2)
    })

    trained_models[model_name] = pipeline

    print("Accuracy:", round(accuracy, 4))
    print("F1 Score:", round(f1, 4))
    print("Training time:", round(training_time, 2), "seconds")
    print("----------------------------------")


# ----------------------------------
# 8. COMPARE THE MODELS
# ----------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="F1 Score",
    ascending=False
).reset_index(drop=True)

results_df.to_csv(RESULTS_PATH, index=False)

print("\nMODEL COMPARISON")
print(results_df.to_string(index=False))


# ----------------------------------
# 9. SAVE THE BEST MODEL
# ----------------------------------

best_model_name = results_df.iloc[0]["Model"]

best_model = trained_models[best_model_name]

joblib.dump(best_model, MODEL_PATH)

print("\nBest model:", best_model_name)
print("Best model saved at:", MODEL_PATH)
print("Comparison results saved at:", RESULTS_PATH)

print("\nTRAINING COMPLETED SUCCESSFULLY!")