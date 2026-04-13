<<<<<<< HEAD
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# =========================
# STEP 1: LOAD THE DATA
# =========================
df = pd.read_csv("crop_practice.csv")

print("First 5 rows:")
print(df.head())
print("\nDataset info:")
print(df.info())

# =========================
# STEP 2: CLEAN THE DATA
# =========================

# Standardize crop names
df["recommended_crop"] = df["recommended_crop"].str.strip().str.title()

# Fill missing numeric values with median
numeric_cols = ["pH", "nitrogen", "phosphorus", "potassium", "organic_matter", "soil_moisture"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(df[col].median())

# Remove impossible values
df = df[(df["pH"] >= 0) & (df["pH"] <= 14)]
df = df[df["nitrogen"] >= 0]
df = df[df["phosphorus"] >= 0]
df = df[df["potassium"] >= 0]
df = df[df["organic_matter"] >= 0]
df = df[df["soil_moisture"] >= 0]

# Drop duplicates
df = df.drop_duplicates()

print("\nCleaned dataset shape:", df.shape)
print("\nMissing values after cleaning:")
print(df.isnull().sum())

# =========================
# STEP 3: ENCODE TEXT COLUMNS
# =========================

soil_encoder = LabelEncoder()
df["soil_type_encoded"] = soil_encoder.fit_transform(df["soil_type"])

crop_encoder = LabelEncoder()
df["crop_encoded"] = crop_encoder.fit_transform(df["recommended_crop"])

# =========================
# STEP 4: SELECT FEATURES AND TARGET
# =========================
X = df[["pH", "nitrogen", "phosphorus", "potassium", "organic_matter", "soil_moisture", "soil_type_encoded"]]
y = df["crop_encoded"]

# =========================
# STEP 5: SPLIT TRAIN AND TEST DATA
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\nTraining set size:", X_train.shape)
print("Testing set size:", X_test.shape)

# =========================
# STEP 6: TRAIN DECISION TREE
# =========================
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

dt_pred = dt_model.predict(X_test)

print("\n===== DECISION TREE RESULTS =====")
print("Accuracy:", accuracy_score(y_test, dt_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, dt_pred))
print("\nClassification Report:\n", classification_report(y_test, dt_pred))

# =========================
# STEP 7: TRAIN RANDOM FOREST
# =========================
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

print("\n===== RANDOM FOREST RESULTS =====")
print("Accuracy:", accuracy_score(y_test, rf_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, rf_pred))
print("\nClassification Report:\n", classification_report(y_test, rf_pred))

# =========================
# STEP 8: CROSS-VALIDATION
# =========================
dt_cv = cross_val_score(dt_model, X, y, cv=5)
rf_cv = cross_val_score(rf_model, X, y, cv=5)

print("\n===== CROSS-VALIDATION =====")
print("Decision Tree CV scores:", dt_cv)
print("Decision Tree Mean CV:", dt_cv.mean())

print("\nRandom Forest CV scores:", rf_cv)
print("Random Forest Mean CV:", rf_cv.mean())

# =========================
# STEP 9: COMPARE AND CHOOSE BEST MODEL
# =========================
dt_acc = accuracy_score(y_test, dt_pred)
rf_acc = accuracy_score(y_test, rf_pred)

if rf_acc >= dt_acc:
    best_model = rf_model
    best_name = "Random Forest"
else:
    best_model = dt_model
    best_name = "Decision Tree"

print(f"\nBest model based on test accuracy: {best_name}")

# =========================
# STEP 10: SAVE THE BEST MODEL
# =========================
joblib.dump(best_model, "best_crop_model.pkl")
joblib.dump(soil_encoder, "soil_encoder.pkl")
joblib.dump(crop_encoder, "crop_encoder.pkl")

print("\nSaved files:")
print("- best_crop_model.pkl")
print("- soil_encoder.pkl")
print("- crop_encoder.pkl")

# =========================
# STEP 11: TEST WITH MANUAL INPUT
# =========================
# manual_input = pd.DataFrame([{
#     "pH": 6.3,
#     "nitrogen": 82,
#     "phosphorus": 38,
#     "potassium": 44,
#     "organic_matter": 3.1,
#     "soil_moisture": 58.0,
#     "soil_type_encoded": soil_encoder.transform(["Loam"])[0]
# }])

manual_input = pd.DataFrame([{
    "pH": 5.8,
    "nitrogen": 95,
    "phosphorus": 42,
    "potassium": 38,
    "organic_matter": 3.8,
    "soil_moisture": 82.0,
    "soil_type_encoded": soil_encoder.transform(["Clay"])[0]
}])

predicted_class = best_model.predict(manual_input)[0]
predicted_crop = crop_encoder.inverse_transform([predicted_class])[0]

print("\n===== MANUAL TEST =====")
print("Predicted crop:", predicted_crop)

# =========================
# STEP 12: SIMPLE CHART
# =========================
df["recommended_crop"].value_counts().plot(kind="bar")
plt.title("Crop Counts")
plt.xlabel("Crop")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
=======
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
df = pd.read_csv("crop_recommendation.csv")

# Optional cleanup
df["label"] = df["label"].astype(str).str.strip().str.title()

# Features and target
X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
y = df["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)

print(f"Accuracy: {acc:.4f}")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("Model saved as model.pkl")
print("Scaler saved as scaler.pkl")
>>>>>>> e1c7c43 (Update files)
