import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

data_path = r'D:\Nano_Sensors_2026\mems_thermal_dataset.csv'

print("--- 1. Loading COMSOL Thermal Dataset ---")


df = pd.read_csv(data_path, comment='%', sep=r'\s+|,', engine='python', header=None)
df = df.dropna(how='all', axis=1).apply(pd.to_numeric, errors='coerce').dropna()

num_cols = df.shape[1]
print(f"Detected Columns in File: {num_cols}")


if num_cols == 2:
    df.columns = ['P_app', 'V_out']
    df['T_amb'] = 573.15  # 300°C default
elif num_cols >= 3:
    df = df.iloc[:, :3]
    df.columns = ['P_app', 'T_amb', 'V_out']


max_p = df['P_app'].abs().max()
if max_p > 1000:
    df['P_kPa'] = df['P_app'] / 1000.0
else:
    df['P_kPa'] = df['P_app']

print("\nDataset Sample:")
print(df.head())
print(f"\nTotal Clean Data Samples Collected: {len(df)}")


X = df[['V_out', 'T_amb']]
y = df['P_kPa']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


print("\n--- 2. Training ML Calibration Model ---")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"\nModel Performance:")
print(f"-> R² Accuracy Score: {r2 * 100:.2f}%")
print(f"-> RMSE Error       : {rmse:.4f} kPa")


test_voltage = df['V_out'].iloc[-1]
test_temp_K = df['T_amb'].iloc[-1]

predicted_pressure_kPa = model.predict([[test_voltage, test_temp_K]])[0]

print("\n--- 3. AI Thermal Drift Compensation Test ---")
print(f"Input Sensor Signal      : {test_voltage:.2f} V")
print(f"Target True Pressure     : {y.iloc[-1]:.2f} kPa")
print(f"AI Calibrated Pressure   : {predicted_pressure_kPa:.2f} kPa")


plt.figure(figsize=(9, 5))
plt.scatter(y_test, y_pred, color='blue', alpha=0.7, label='AI Calibrated Output')
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Ideal 1:1 Calibration Line')
plt.title('MEMS Sensor AI Thermal Drift Calibration Result')
plt.xlabel('True Applied Pressure (kPa)')
plt.ylabel('AI Corrected Calibrated Pressure (kPa)')
plt.legend()
plt.grid(True)
plt.savefig(r'D:\Nano_Sensors_2026\AI_Calibration_Result.png', dpi=300)
print("\nPlot saved successfully as 'AI_Calibration_Result.png'!")
plt.show()