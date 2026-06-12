# Trains the SVM diabetes model and saves artifacts to backend/model/.

import json
import pickle
from pathlib import Path

import pandas as pd
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

TRAINING_DIR = Path(__file__).resolve().parent
MODEL_DIR = TRAINING_DIR.parent / "backend" / "model"


def main():
    dataset = pd.read_csv(TRAINING_DIR / "diabetes.csv")
    features = dataset.drop(columns="Outcome", axis=1)
    labels = dataset["Outcome"]

    scaler = StandardScaler()
    scaler.fit(features)

    train_x, test_x, train_y, test_y = train_test_split(
        scaler.transform(features),
        labels,
        test_size=0.2,
        stratify=labels,
        random_state=1234,
    )

    classifier = svm.SVC(kernel="linear")
    classifier.fit(train_x, train_y)

    train_accuracy = accuracy_score(classifier.predict(train_x), train_y)
    test_accuracy = accuracy_score(classifier.predict(test_x), test_y)
    print(f"Train accuracy: {train_accuracy:.4f}")
    print(f"Test accuracy:  {test_accuracy:.4f}")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    with open(MODEL_DIR / "diabetes_prediction.pickle", "wb") as model_file:
        pickle.dump(classifier, model_file)

    with open(MODEL_DIR / "scaler.pickle", "wb") as scaler_file:
        pickle.dump(scaler, scaler_file)

    columns = {"data_columns": [col.lower() for col in features.columns]}
    with open(MODEL_DIR / "columns.json", "w") as columns_file:
        json.dump(columns, columns_file)

    print(f"Model files saved to {MODEL_DIR}")


if __name__ == "__main__":
    main()
