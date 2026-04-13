import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score
# LOAD DATASETS
# ============================================================

if os.path.exists("diabetes.csv"):
    diabetes_df = pd.read_csv("diabetes.csv", names=[
        "Pregnancies","Glucose","BloodPressure","SkinThickness",
        "Insulin","BMI","DiabetesPedigreeFunction","Age","Outcome"
    ])
else:
    print("⚠️ diabetes.csv not found")

if os.path.exists("heart.csv"):
    heart_df = pd.read_csv("heart.csv")
else:
    print("⚠️ heart.csv not found")

for col in heart_df.columns:
    if heart_df[col].dtype.name in ["object", "str"]:
        heart_df[col] = heart_df[col].astype("category").cat.codes

# ============================================================
# MODEL TRAINING
# ============================================================

X_heart = heart_df.drop("target", axis=1)
y_heart = heart_df["target"]
X_diabetes = diabetes_df.drop("Outcome", axis=1)
y_diabetes = diabetes_df["Outcome"]

Xh_train,Xh_test,yh_train,yh_test = train_test_split(X_heart,y_heart,test_size=0.2,random_state=42)
Xd_train,Xd_test,yd_train,yd_test = train_test_split(X_diabetes,y_diabetes,test_size=0.2,random_state=42)

heart_model = RandomForestClassifier(n_estimators=200, random_state=42)
heart_model.fit(Xh_train, yh_train)
diabetes_model = RandomForestClassifier(n_estimators=200, random_state=42)
diabetes_model.fit(Xd_train, yd_train)

heart_acc     = accuracy_score(yh_test, heart_model.predict(Xh_test))
diabetes_acc  = accuracy_score(yd_test, diabetes_model.predict(Xd_test))
heart_cm      = confusion_matrix(yh_test, heart_model.predict(Xh_test))
diabetes_cm   = confusion_matrix(yd_test, diabetes_model.predict(Xd_test))
