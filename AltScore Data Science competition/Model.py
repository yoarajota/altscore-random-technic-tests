import pandas as pd
import h3
from shapely.geometry import Point
import geopandas as gpd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

# 1. Load Data
# Using parquet for mobility data (efficient for large datasets)
device_data = pd.read_parquet('data/mobility_data.parquet')  # device_id, lat, lon, timestamp
train_data = pd.read_csv('data/train.csv')                   # hex_id, cost_of_living
submission_data = pd.read_csv('data/test.csv')              # hex_id

# 2. Convert Lat/Lon to H3 Hexagons
def latlon_to_h3(row, resolution=8):
    try:
        return h3.latlng_to_cell(row['lat'], row['lon'], resolution)
    except:
        return None  # Handle invalid lat/lon values

# Apply H3 conversion
device_data['hex_id'] = device_data.apply(latlon_to_h3, axis=1, resolution=8)

# Drop rows with invalid H3 indices (if any)
device_data = device_data.dropna(subset=['hex_id'])

# 3. Feature Engineering from Device Data
# Number of device records per hexagon
hex_counts = device_data.groupby('hex_id').size().reset_index(name='device_count')

# Number of unique devices per hexagon
unique_devices = device_data.groupby('hex_id')['device_id'].nunique().reset_index(name='unique_devices')

# Additional features: Night activity ratio (assuming timestamp is available)
device_data['timestamp'] = pd.to_datetime(device_data['timestamp'], errors='coerce')
device_data['hour'] = device_data['timestamp'].dt.hour
device_data['is_night'] = device_data['hour'].apply(lambda x: 1 if 0 <= x < 6 or 18 <= x < 24 else 0)
night_activity = device_data.groupby('hex_id')['is_night'].mean().reset_index(name='night_activity_ratio')

# Merge all device-based features
features = hex_counts.merge(unique_devices, on='hex_id', how='left')
features = features.merge(night_activity, on='hex_id', how='left')

# 4. Merge Features with Train and Submission Data
# Merge with train_data
train_features = train_data.merge(features, on='hex_id', how='left')

# Merge with submission_data
submission_features = submission_data.merge(features, on='hex_id', how='left')

# 5. Prepare Data for Modeling
# Features (X) and target (y) for training
X = train_features.drop(columns=['hex_id', 'cost_of_living'])
y = train_features['cost_of_living']

# Handle missing values (impute with mean for numerical features)
X.fillna(X.mean(), inplace=True)

# Split data for validation
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Train Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_val)
rmse = np.sqrt(mean_squared_error(y_val, y_pred))
print(f"Validation RMSE: {rmse}")

# 7. Predict for Submission
# Prepare submission features
X_submission = submission_features.drop(columns=['hex_id'])
X_submission.fillna(X_submission.mean(), inplace=True)

# Predict and clip predictions to [0, 1]
submission_features['cost_of_living'] = model.predict(X_submission)
submission_features['cost_of_living'] = submission_features['cost_of_living'].clip(0, 1)

# Create submission file
submission = submission_features[['hex_id', 'cost_of_living']]
submission.to_csv('submission.csv', index=False)
print("Submission file created: submission.csv")

# 8. Feature Importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(importance)

# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(importance['feature'], importance['importance'], color='skyblue')
plt.xlabel('Importance')
plt.title('Feature Importance')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# 9. Save Features for Reproducibility (optional, using parquet for efficiency)
train_features.to_parquet('data/train_features.parquet')
submission_features.to_parquet('data/submission_features.parquet')