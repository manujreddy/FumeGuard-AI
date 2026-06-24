#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// --- 1. YOUR WIFI DETAILS ---
const char* ssid = "realmep3ultra";
const char* password = "11111111";

// --- 2. YOUR HIVEMQ DETAILS ---
const char* mqtt_server = "4954d9a4497f45f0a20cb718ea18164a.s1.eu.hivemq.cloud"; 
const char* mqtt_username = "esp123";
const char* mqtt_password = "Hello1234";
const int mqtt_port = 8883;

// --- 3. HARDWARE PINS ---
const int mq135_pin = 34;       // Gas sensor 1 (Air Quality)
const int mq2_pin = 35;         // Gas sensor 2 (Smoke/Flammables)
#define DHTPIN 32               
#define DHTTYPE DHT11           
DHT dht(DHTPIN, DHTTYPE);

WiFiClientSecure espClient; 
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  dht.begin(); 
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(1000); }
  
  espClient.setInsecure(); 
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    while (!client.connected()) {
      if (client.connect("ESP32_FumeGuard", mqtt_username, mqtt_password)) {
        // Connected
      } else { delay(3000); }
    }
  }
  client.loop();

  // --- READ ALL SENSORS ---
  float temp = dht.readTemperature();
  int mq135_value = analogRead(mq135_pin);
  int mq2_value = analogRead(mq2_pin); // Read the second sensor!
  
  // --- PACKAGE AND SEND DATA ---
  StaticJsonDocument<200> doc;
  doc["mq135"] = mq135_value;
  doc["mq2"] = mq2_value;
  
  if (!isnan(temp)) {
    doc["temp"] = temp;
  } else {
    doc["temp"] = 25.0; 
  }
  
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer);
  client.publish("fumeguard/sensors", jsonBuffer);
  
  delay(2000);
}