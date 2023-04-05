// mtg

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Arduino_JSON.h>
#include <Stepper.h>

const char* ssid = "thegunduboss";
const char* password = "password";

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

#define IN1 14 // D5
#define IN2 12 // D6
#define IN3 13 // D7
#define IN4 15 // D8
#define LOCK 5 // D1

const int stepsPerRevolution = 2000;
Stepper myStepper(stepsPerRevolution, IN1, IN2, IN3, IN4);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);

  myStepper.setSpeed(60);
  pinMode(LOCK, OUTPUT);
  digitalWrite(LOCK, HIGH);

  Serial.println("hihihihihihi");

  ESP.eraseConfig();
  WiFi.mode(WIFI_STA); //Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while(WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP8266 IP: ");
  Serial.println(WiFi.localIP());

  WiFi.setSleepMode(WIFI_NONE_SLEEP);
}

void loop() {
  // return;
  if ((millis() - lastTime) > timerDelay) {
    // Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      String serverPath = serverName;
      
      jsonBuffer = httpGETRequest(serverPath.c_str());
      if (jsonBuffer == "{}") return;
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
        if (flag != prev) {
          for(int i=0; i<5; i++) forward();
          lock();          
          // couple();
        }
        else Serial.println("error in 1 check");
      }
      else if (!strcmp(myObject["feeds"][0]["field1"], "0")) {
        flag = 0;
        if (flag != prev) {
          unlock();
          for(int i=0; i<5; i++) backward();
          // decouple();        
        }
        else Serial.println("error in 2 check");
      }
    }
    else {
      Serial.println("WiFi Disconnected");
      // Serial.println("Reconnecting");
      // WiFi.reconnect();
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

void forward() {
  prev = 1;
  Serial.println("forward");
  myStepper.step(1.06 * stepsPerRevolution);
}

void backward() {
  prev = 0;
  Serial.println("backward");
  myStepper.step(-1.06 * stepsPerRevolution);
}

void lock() {
  prev = 1;
  Serial.println("lock");
  digitalWrite(LOCK, LOW);
}

void unlock() {
  prev = 0;
  Serial.println("unlock");
  digitalWrite(LOCK, HIGH);
}

void couple() {
  prev = 1;
  Serial.println("coupling");
  for(int i=0; i<5; i++) {
    myStepper.step(1.06 * stepsPerRevolution);
  }
  // yield();
  delay(10);
  digitalWrite(LOCK, HIGH);
  // yield();
}

void decouple() {
  prev = 0;
  Serial.println("decoupling");
  digitalWrite(LOCK, LOW);
  delay(10);
  for(int i=0; i<5; i++) {
    myStepper.step(-1.06 * stepsPerRevolution);
  }
  // yield();
}