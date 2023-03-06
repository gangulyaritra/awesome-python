import sys
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
import mlflow
import mlflow.sklearn


# Set Registry URI, i.e., where MLflow saves runs.

mlflow.set_tracking_uri(r"/home/dimpu/Documents/mlflow/mlruns")

# mlflow.set_tracking_uri("http://ec2-65-2-182-71.ap-south-1.compute.amazonaws.com:5000/")

print("Artifact Store:", mlflow.get_artifact_uri())


# Load Dataset.
data = pd.read_csv(r"/home/dimpu/Documents/mlflow/data/aug_train.csv")
targets = data[["target"]]


# Data Preprocessing and Feature Engineering.
data.drop(["enrollee_id", "target"], inplace=True, axis=1)

categorical_features = []
numerical_features = []

for column in data.columns:
    dtype = str(data[column].dtype)
    if dtype in {"float64", "int64"}:
        numerical_features.append(column)
    else:
        categorical_features.append(column)

for categorical_feature in categorical_features:
    data[categorical_feature].fillna("missing", inplace=True)
    le = LabelEncoder()
    data[categorical_feature] = le.fit_transform(data[categorical_feature])


# Split Dataset into Train and Test Set.
X_train, X_test, y_train, y_test = train_test_split(
    data.values,
    targets.values.ravel(),
    test_size=0.3,
    random_state=42,
    stratify=targets.values,
)

alpha = sys.argv[0] if len(sys.argv) > 1 else 0.5

mlflow.set_experiment("training experiment")

# Hyperparameters Tuning.
n_estimators_range = np.arange(100, 300, 25)
max_depth_range = np.arange(1, 25, 2)
max_features_range = ["sqrt", None, "log2"]


# Model Training with MLflow.
for n_estimators in tqdm(n_estimators_range):
    for max_depth in tqdm(max_depth_range, leave=False):
        for max_features in tqdm(max_features_range, leave=False):
            with mlflow.start_run(nested=True):
                model = RandomForestClassifier(
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    max_features=max_features,
                    n_jobs=3,
                )

                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred)
                auc = roc_auc_score(y_test, y_pred)

                mlflow.log_param("n_estimators", n_estimators)
                mlflow.log_param("max_depth", max_depth)
                mlflow.log_param("max_features", max_features)

                mlflow.log_metric("Accuracy", accuracy)
                mlflow.log_metric("Precision", precision)
                mlflow.log_metric("Recall", recall)
                mlflow.log_metric("F1", f1)
                mlflow.log_metric("AUC", auc)

                mlflow.sklearn.log_model(model, "model")
