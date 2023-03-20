#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Arduino_JSON.h>
#include <Stepper.h>

const char* ssid = "RoboSAR2";
const char* password = "robosar2022";

WiFiClient client;

char   host[]      = "api.thingspeak.com"; // ThingSpeak address
String APIkey      = "2064160";             // Thingspeak Read Key, works only if a PUBLIC viewable channel
String APIreadkey  = "SK4O1YEHVBXIWABJ";   // Thingspeak Read Key, works only if a PUBLIC viewable channel
const int httpPort = 80;

String serverName = "http://api.thingspeak.com/channels/" + APIkey + "/fields/1.json?api_key=" + APIreadkey + "&results=1";

unsigned long lastTime = 0;
unsigned long timerDelay = 1000;

String jsonBuffer;
int flag;
int prev = 0;

#define IN1 32
#define IN2 33
#define IN3 34
#define IN4 35
#define PIN 25

const int stepsPerRevolution = 2000;
Stepper myStepper(stepsPerRevolution, IN1, IN2, IN3, IN4);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);

  myStepper.setSpeed(60);
  pinMode(PIN, OUTPUT);

  WiFi.mode(WIFI_STA); //Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while(WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());

}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    // Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      String serverPath = serverName;
      
      jsonBuffer = httpGETRequest(serverPath.c_str());
      // Serial.println(jsonBuffer);
      JSONVar myObject = JSON.parse(jsonBuffer);
  
      // JSON.typeof(jsonVar) can be used to get the type of the var
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return;
      }
    
      Serial.print("Couple flag: ");
      Serial.println(myObject["feeds"][0]["field1"]);
      Serial.println(JSON.typeof(myObject["feeds"][0]["field1"]));
      if (!strcmp(myObject["feeds"][0]["field1"], "1")) {
        flag = 1;
        if (flag != prev)
          couple();
        else Serial.println("error in 1 check");
      }
      else if (!strcmp(myObject["feeds"][0]["field1"], "0")) {
        flag = 0;
        if (flag != prev)
          decouple();        
        else Serial.println("error in 2 check");
      }
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}

String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;
    
  // Your Domain name with URL path or IP address with path
  http.begin(client, serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "{}"; 
  
  if (httpResponseCode>0) {
    // Serial.print("HTTP Response code: ");
    // Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}

void couple() {
  prev = 1;
  Serial.println("coupling");
  return;
}

void decouple() {
  prev = 0;
  Serial.println("decoupling");
  return;  
}