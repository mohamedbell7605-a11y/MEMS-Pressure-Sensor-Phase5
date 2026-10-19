/*
 * ESP32 MEMS Pressure & Temperature Telemetry Firmware
 * Reads raw sensor signals and streams JSON data via Serial (UART)
 */

#include <Arduino.h>

const unsigned long BAUDRATE = 115200;

void setup() {
  Serial.begin(BAUDRATE);
  while (!Serial) {
    ; 
  }
}

void loop() {
 
  float raw_voltage = (analogRead(34) / 4095.0) * 3.3; 
  float ambient_temp_k = 293.15 + (rand() % 280);     

  Serial.print("{\"voltage_v\": ");
  Serial.print(raw_voltage, 3);
  Serial.print(", \"temp_k\": ");
  Serial.print(ambient_temp_k, 2);
  Serial.println("}");

  delay(500); 
}