// ESP32 Sensor Data Collection & MQTT Publishing
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "broker.hivemq.com"; // Or your configured broker

#define DHTPIN 4
#define DHTTYPE DHT11
#define LDRPIN 34
#define TRIGPIN 5
#define ECHOPIN 18

DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(TRIGPIN, OUTPUT);
  pinMode(ECHOPIN, INPUT);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    while (!client.connected()) {
      client.connect("ESP32_Client");
    }
  }
  client.loop();

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int light = analogRead(LDRPIN);

  digitalWrite(TRIGPIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW);
  float duration = pulseIn(ECHOPIN, HIGH);
  float distance = duration * 0.034 / 2;

  String payload = "{\"temperature\":" + String(temp) + 
                   ",\"humidity\":" + String(hum) + 
                   ",\"light\":" + String(light) + 
                   ",\"distance\":" + String(distance) + "}";

  client.publish("lab/telemetry", payload.c_str());
  delay(2000);
}
