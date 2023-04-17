// mtg adafruit-io

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Arduino_JSON.h>
#include <ESP8266WiFiMulti.h>
#include <Stepper.h>
#include <WiFiClientSecureBearSSL.h>

const char* ssid = "ESP-Net";
const char* password = "robosar2022";

WiFiClient client;
ESP8266WiFiMulti WiFiMulti;

String IO_USERNAME = "ysudhansh";
String IO_KEY = "aio_FNkZ38Hy1iXvCb7n1Pk0nqxWRav9";

// 114: 0, 115: 1, 116: 2
String robot_names[3] = {"k114", "k115", "k116"};
int robot_num = 1;
// https://io.adafruit.com/api/v2/ysudhansh/feeds/mtg-mechanism.k114/data/last?x-aio-key=aio_FNkZ38Hy1iXvCb7n1Pk0nqxWRav9
String serverName = "https://io.adafruit.com/api/v2/" + IO_USERNAME + "/feeds/mtg-mechanism." + robot_names[robot_num] + "/data/last.json?x-aio-key=" + IO_KEY;
// String field_name = "field" + field_num;

unsigned long lastTime = 0;
unsigned long timerDelay = 100;

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

  Serial.println("\nhihihihihihi");
  Serial.println(serverName);

  ESP.eraseConfig();+
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
      
      jsonBuffer = httpsGETRequest(serverPath.c_str());
      // Serial.println(jsonBuffer);
      if (jsonBuffer == "{}") return;
      JSONVar myObject = JSON.parse(jsonBuffer);
  
      // JSON.typeof(jsonVar) can be used to get the type of the var
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return;
      }

      if (!strcmp(myObject["value"], "0")) {
        flag = 0;
        if (flag != prev) {
          Serial.println("decouple");
          decouple();        
          motorOff();
        }
        else Serial.println("repeat in decoupling check");
      }
      else if (!strcmp(myObject["value"], "1")) {
        flag = 1;
        if (flag != prev) {      
          Serial.println("couple"); 
          couple();
          motorOff();
        }
        else Serial.println("repeat in coupling check");
      }
      else if (!strcmp(myObject["value"], "2")) {
        flag = 2;
        if (flag != prev) {
          Serial.println("forward"); 
          forward();     
          motorOff();
        }
        else Serial.println("repeat in forward check");
      }
      else if (!strcmp(myObject["value"], "3")) {
        flag = 3;
        if (flag != prev) {
          Serial.println("backward"); 
          backward();        
          motorOff();
        }
        else Serial.println("repeat in backward check");
      }
      else if (!strcmp(myObject["value"], "4")) {
        flag = 4;
        if (flag != prev) {
          Serial.println("lock"); 
          lock();        
        }
        else Serial.println("repeat in lock check");
      }
      else if (!strcmp(myObject["value"], "5")) {
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

String httpsGETRequest(const char* serverName) {
  // WiFiClient client;
  HTTPClient https;

  std::unique_ptr<BearSSL::WiFiClientSecure> client(new BearSSL::WiFiClientSecure);
  client->setInsecure();
    
  // Your Domain name with URL path or IP address with path
  https.begin(*client, serverName);
  
  // Send HTTP POST request
  int httpsResponseCode = https.GET();
  
  String payload = "{}"; 
  
  if (httpsResponseCode>0) {
    payload = https.getString();
  }
  else {
    Serial.print("repeat code: ");
    Serial.println(httpsResponseCode);
  }
  // Free resources
  https.end();

  return payload;
}

void forward() {
  myStepper.step(1.06 * stepsPerRevolution);
  delay(100);
}

void backward() {
  myStepper.step(-1.06 * stepsPerRevolution);
  delay(100);
}

void lock() {
  delay(3000);
  digitalWrite(LOCK, LOW);
}

void unlock() {
  delay(3000);
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