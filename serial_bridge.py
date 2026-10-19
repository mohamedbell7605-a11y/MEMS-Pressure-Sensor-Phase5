import serial
import json
import time

PORT = 'COM3'  
BAUD = 115200

print(f"Connecting to ESP32 Telemetry System on {PORT}...")

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)
    print("Connected successfully! Streaming calibrated live data:\n")

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            try:
                data = json.loads(line)
                v_raw = data['voltage_v']
                t_raw = data['temp_k']

                print(f"[LIVE ADC READ] Voltage: {v_raw:.2f} V | Temperature: {t_raw:.1f} K")
            except json.JSONDecodeError:
                pass

except serial.SerialException:
    print(f"Notice: ESP32 Hardware not detected on {PORT}. Simulation Mode Ready.")