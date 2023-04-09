// mtg

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

// 114: 1, 115: 2, 116: 3
String serverName = "http://api.thingspeak.com/channels/" + APIkey + "/fields/2.json?api_key=" + APIreadkey + "&results=1";
String field_name = "field2";

unsigned long lastTime = 0;
unsigned long timerDelay = 1000;

String jsonBuffer;
int flag = 0;
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
  digitalWrite(LOCK, LOW);
  motorOff();

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
  if ((millis() - lastTime) > timerDelay) {
    // Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      String serverPath = serverName;
      
      jsonBuffer = httpGETRequest(serverPath.c_str());
      if (jsonBuffer == "{}") return;
      JSONVar myObject = JSON.parse(jsonBuffer);
  
      // JSON.typeof(jsonVar) can be used to get the type of the var
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return;
      }

      if (!strcmp(myObject["feeds"][0][field_name], "0")) {
        flag = 0;
        if (flag != prev) {
          Serial.println("decouple");
          decouple();        
          motorOff();
        }
        else Serial.println("repeat in decoupling check");
      }
      else if (!strcmp(myObject["feeds"][0][field_name], "1")) {
        flag = 1;
        if (flag != prev) {      
          Serial.println("couple"); 
          couple();
          motorOff();
        }
        else Serial.println("repeat in coupling check");
      }
      else if (!strcmp(myObject["feeds"][0][field_name], "2")) {
        flag = 2;
        if (flag != prev) {
          Serial.println("forward"); 
          forward();     
          motorOff();
        }
        else Serial.println("repeat in forward check");
      }
      else if (!strcmp(myObject["feeds"][0][field_name], "3")) {
        flag = 3;
        if (flag != prev) {
          Serial.println("backward"); 
          backward();        
          motorOff();
        }
        else Serial.println("repeat in backward check");
      }
      else if (!strcmp(myObject["feeds"][0][field_name], "4")) {
        flag = 4;
        if (flag != prev) {
          Serial.println("lock"); 
          lock();        
        }
        else Serial.println("repeat in lock check");
      }
      else if (!strcmp(myObject["feeds"][0][field_name], "5")) {
        flag = 5;
        if (flag != prev) {
          Serial.println("unlock"); 
          unlock();        
        }
        else Serial.println("repeat in unlock check");
      }
      prev = flag;
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
    payload = http.getString();
  }
  else {
    Serial.print("repeat code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}

void forward() {
  myStepper.step(1.1 * stepsPerRevolution);
  delay(100);
}

void backward() {
  myStepper.step(-1.1 * stepsPerRevolution);
  delay(100);
}

void lock() {
  digitalWrite(LOCK, LOW);
}

void unlock() {
  digitalWrite(LOCK, HIGH);
}

void couple() {
  unlock();
  for(int i=0; i<5; i++) forward();
  lock();
}

void decouple() {
  unlock();
  for(int i=0; i<5; i++) backward();
  lock();
}

void motorOff() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}