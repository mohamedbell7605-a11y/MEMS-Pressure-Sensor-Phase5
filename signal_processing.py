import numpy as np
import matplotlib.pyplot as plt

#1. Generating a time signal and a dynamic pressure signal (0 to 100 kPa)
time = np.linspace(0, 10, 500)
pressure = 50 + 40 * np.sin(2 * np.pi * 0.2 * time)

#2. Signal Conditioning (Converting pressure into voltage) (0-100 kPa gives 0-5 V)
ideal_voltage = (pressure / 100.0) * 5.0

#3. Adding Gaussian Noise
np.random.seed(42)
noise = np.random.normal(loc=0.0, scale=0.25, size=time.shape)
noisy_voltage = ideal_voltage + noise

# 4.Moving Average Filter)
window_size = 15
kernel = np.ones(window_size) / window_size
filtered_voltage = np.convolve(noisy_voltage, kernel, mode='same')

# 5. Plotting the graphical results
plt.figure(figsize=(10, 5), dpi=150)
plt.plot(time, noisy_voltage, label='Noisy Raw Signal (Sensor ADC Input)', color='salmon', alpha=0.7, linewidth=1)
plt.plot(time, ideal_voltage, label='Ideal MEMS Signal (COMSOL Output)', color='black', linestyle='--', linewidth=1.5)
plt.plot(time, filtered_voltage, label=f'Filtered Signal (Moving Avg N={window_size})', color='navy', linewidth=2)

plt.title('MEMS Pressure Sensor - Signal Conditioning & Noise Reduction (Phase 5)', fontsize=12, fontweight='bold')
plt.xlabel('Time (seconds)', fontsize=10)
plt.ylabel('Amplified Output Voltage (V DC)', fontsize=10)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(loc='upper right')
plt.tight_layout()

# 6. Save the image to the workspace
plt.savefig('Filtered_Signal_Phase5.png', dpi=300)
print("Processing complete! Graph saved as 'Filtered_Signal_Phase5.png'")
plt.show()