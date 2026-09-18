import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

def load_data(filepath="data/processed/feature_table.csv"):
    return pd.read_csv(filepath)

def train_and_evaluate(df, model_save_path="models/random_forest_model.pkl"):
    print("Preparing data...")
    # X = all columns except user, label; y = label
    drop_cols = ["user", "label"] if "user" in df.columns else ["label"]
    X = df.drop(columns=drop_cols, errors="ignore")
    y = df["label"]

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Training RandomForestClassifier...")
    clf = RandomForestClassifier(n_estimators=200, max_depth=10, class_weight="balanced", random_state=42)
    clf.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    
    print(f"Saving model to {model_save_path}...")
    joblib.dump(clf, model_save_path)
    print("Model saved successfully.")
    
    return clf, acc, prec, rec, f1

if __name__ == "__main__":
    df = load_data()
    train_and_evaluate(df)
