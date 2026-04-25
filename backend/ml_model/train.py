import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# Create a more comprehensive dataset for crop prediction
np.random.seed(42)

# Generate synthetic data for different crops
n_samples = 1000

# Crop types and their typical conditions
crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean', 'Potato', 'Tomato']

# Generate data based on crop requirements
data = []
for crop in crops:
    if crop == 'Rice':
        rainfall = np.random.normal(150, 30, n_samples//len(crops))
        temperature = np.random.normal(25, 5, n_samples//len(crops))
        humidity = np.random.normal(80, 10, n_samples//len(crops))
        soil_ph = np.random.normal(6.5, 0.5, n_samples//len(crops))
    elif crop == 'Wheat':
        rainfall = np.random.normal(75, 20, n_samples//len(crops))
        temperature = np.random.normal(20, 5, n_samples//len(crops))
        humidity = np.random.normal(60, 15, n_samples//len(crops))
        soil_ph = np.random.normal(6.0, 0.5, n_samples//len(crops))
    elif crop == 'Maize':
        rainfall = np.random.normal(100, 25, n_samples//len(crops))
        temperature = np.random.normal(25, 5, n_samples//len(crops))
        humidity = np.random.normal(70, 15, n_samples//len(crops))
        soil_ph = np.random.normal(6.0, 0.5, n_samples//len(crops))
    elif crop == 'Cotton':
        rainfall = np.random.normal(80, 20, n_samples//len(crops))
        temperature = np.random.normal(28, 5, n_samples//len(crops))
        humidity = np.random.normal(65, 15, n_samples//len(crops))
        soil_ph = np.random.normal(6.5, 0.5, n_samples//len(crops))
    elif crop == 'Sugarcane':
        rainfall = np.random.normal(150, 30, n_samples//len(crops))
        temperature = np.random.normal(27, 5, n_samples//len(crops))
        humidity = np.random.normal(75, 15, n_samples//len(crops))
        soil_ph = np.random.normal(6.5, 0.5, n_samples//len(crops))
    elif crop == 'Soybean':
        rainfall = np.random.normal(90, 20, n_samples//len(crops))
        temperature = np.random.normal(24, 5, n_samples//len(crops))
        humidity = np.random.normal(70, 15, n_samples//len(crops))
        soil_ph = np.random.normal(6.0, 0.5, n_samples//len(crops))
    elif crop == 'Potato':
        rainfall = np.random.normal(70, 15, n_samples//len(crops))
        temperature = np.random.normal(18, 4, n_samples//len(crops))
        humidity = np.random.normal(75, 15, n_samples//len(crops))
        soil_ph = np.random.normal(5.5, 0.5, n_samples//len(crops))
    elif crop == 'Tomato':
        rainfall = np.random.normal(60, 15, n_samples//len(crops))
        temperature = np.random.normal(22, 5, n_samples//len(crops))
        humidity = np.random.normal(65, 15, n_samples//len(crops))
        soil_ph = np.random.normal(6.0, 0.5, n_samples//len(crops))

    crop_data = pd.DataFrame({
        'rainfall': rainfall,
        'temperature': temperature,
        'humidity': humidity,
        'soil_ph': soil_ph,
        'crop': [crop] * len(rainfall)
    })
    data.append(crop_data)

# Combine all data
df = pd.concat(data, ignore_index=True)

# Ensure we have equal samples per crop
df = df.groupby('crop').head(n_samples//len(crops)).reset_index(drop=True)

# Features and target
X = df[['rainfall', 'temperature', 'humidity', 'soil_ph']]
y = df['crop']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2%}")

# Save model
model_path = os.path.join(os.path.dirname(__file__), 'crop_model.pkl')
joblib.dump(model, model_path)

print(f"✅ Enhanced ML model trained and saved as {model_path}")
print(f"Features: {list(X.columns)}")
print(f"Crops: {crops}")