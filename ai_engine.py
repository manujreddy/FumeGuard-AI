import paho.mqtt.client as mqtt
import json
import ssl
import numpy as np
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier

# --- 1. YOUR HIVEMQ DETAILS ---
broker = "4954d9a4497f45f0a20cb718ea18164a.s1.eu.hivemq.cloud" 
port = 8883
username = "esp123"
password = "Hello1234"
sensor_topic = "fumeguard/sensors"

# Create a clean CSV file to store data for the dashboard
if not os.path.exists('live_data.csv'):
    pd.DataFrame(columns=['Time', 'AQI', 'Temp', 'GasType', 'FanSpeed']).to_csv('live_data.csv', index=False)

reading_count = 0

# --- 2. THE ELECTRONIC NOSE (AI CLASSIFIER) ---
print("Training Electronic Nose AI...")
# We use synthetic ratios to teach the AI what different gases look like
# Format: [MQ-135 (Air Quality), MQ-2 (Flammable/Smoke)]
X_train = np.array([
    [300, 200], [350, 220], [400, 250], # Normal Air (Low values)
    [800, 950], [850, 1000], [900, 1100], # Smoke / Fire (MQ-2 spikes much higher)
    [900, 400], [950, 450], [1000, 500]   # Chemical Vapor / CO2 (MQ-135 spikes much higher)
])
y_train = np.array([
    "Clean Air", "Clean Air", "Clean Air",
    "Smoke / Combustible", "Smoke / Combustible", "Smoke / Combustible",
    "Toxic Chemical Vapor", "Toxic Chemical Vapor", "Toxic Chemical Vapor"
])

# Train the Random Forest AI
electronic_nose = RandomForestClassifier(n_estimators=10, random_state=42)
electronic_nose.fit(X_train, y_train)
print("✅ Electronic Nose Calibrated and Ready!")

# --- 3. CONVERSION & CONTROL MATH ---
def calculate_aqi(mq135_val, temp):
    # Temperature compensation
    if temp > 25:
        mq135_val = mq135_val * (1.0 - ((temp - 25) * 0.01))
    
    # Establish a "Clean Air" baseline for the ESP32 analog pin
    # Normally, clean air reads between 100 and 200 on the ESP32
    baseline = 150 
    
    if mq135_val <= baseline:
        # If the air is very clean, map it smoothly between 0 and 30 AQI
        aqi = (mq135_val / baseline) * 30 
    else:
        # If gas is detected, scale it up realistically 
        # Every 4 raw points adds 1 AQI point
        aqi = 30 + ((mq135_val - baseline) * 0.25)
    
    # Keep AQI strictly between 0 and 500
    return max(0, min(500, aqi))

def calculate_proportional_fan(aqi):
    # If air is good (AQI under 50), fan is OFF
    if aqi < 50:
        return 0
    # If air is hazardous (AQI over 200), fan is 100% MAX
    elif aqi >= 200:
        return 100
    # If air is in between, scale the fan smoothly!
    else:
        # Maps an AQI of 50-200 to a Fan Speed of 20%-100%
        speed = 20 + ((aqi - 50) / 150) * 80
        return int(speed)

# --- 4. MQTT MESSAGE HANDLING ---
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Connected to Cloud Brain! Listening for sensors...")
        client.subscribe(sensor_topic)

def on_message(client, userdata, msg):
    global reading_count
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        
        # We need both sensors for the AI Nose!
        mq135_raw = data.get("mq135", 400)
        mq2_raw = data.get("mq2", 200) 
        temp = data.get("temp", 25.0)
        
        reading_count += 1
        
        # 1. Calculate Standard AQI
        aqi = calculate_aqi(mq135_raw, temp)
        
        # 2. Use AI to guess the gas type based on the two sensor readings
        gas_type_prediction = electronic_nose.predict([[mq135_raw, mq2_raw]])[0]
        
        # 3. Calculate smooth fan speed
        fan_speed_percent = calculate_proportional_fan(aqi)

        # 4. Save to CSV for the Dashboard
        new_row = pd.DataFrame({
            'Time': [reading_count], 
            'AQI': [aqi], 
            'Temp': [temp], 
            'GasType': [gas_type_prediction], 
            'FanSpeed': [fan_speed_percent]
        })
        new_row.to_csv('live_data.csv', mode='a', header=False, index=False)
        
        print(f"AQI: {aqi:.0f} | AI Detects: {gas_type_prediction} | Auto-Fan Output: {fan_speed_percent}%")
            
    except Exception as e:
        pass

# --- SETUP MQTT CLIENT ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "FumeGuard_Engine")
client.username_pw_set(username, password)
client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT) 
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.loop_forever()