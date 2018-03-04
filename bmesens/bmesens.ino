/*
SPIFFS-served REST API example for PersWiFiManager v3.0
*/

#define DEBUG_SERIAL //uncomment for Serial debugging statements
#ifdef DEBUG_SERIAL
#define DEBUG_BEGIN Serial.begin(115200)
#define DEBUG_PRINT(x) Serial.println(x)
#else
#define DEBUG_PRINT(x)
#define DEBUG_BEGIN
#endif

struct tcp_pcb;
extern struct tcp_pcb* tcp_tw_pcbs;
extern "C" void tcp_abort (struct tcp_pcb* pcb);

/* Libs for I2C and BME280 sensor lib */
#include <Wire.h>
#include <BME280I2C.h>
BME280I2C bme;

/* Import ESP32 Wifi Stack */
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>

//* Easy web interface to setup without reprogramming *//
#include <PersWiFiManager.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>

//* Makes the device discoverable in Windows Expoler *//
#include <EasySSDP.h>

//* WebServer Extension to serve files directly from SPIFF *//
#include <SPIFFSReadServer.h> 

#include <DNSServer.h>
#include <FS.h>
#define DEVICE_NAME "ESP8266 DEVICE"


//* Createing server objects *//
SPIFFSReadServer server(80);
DNSServer dnsServer;
PersWiFiManager persWM(server, dnsServer);

//* RealTime data Global *//
float tempValue, humValue;
int x;
String y;
String eszkozid = "alapid";
String ipaddr1 = "alapip";
String ipaddr2 = "alapip";
int port1 = 0;
int port2 = 0;
int refreshrate = 1;
unsigned long int stopper = 0;
bool firstAlert = true;

void setup() {
  DEBUG_BEGIN; //for terminal debugging
  DEBUG_PRINT();

  //* RELAYS *//
  pinMode(D5, OUTPUT);
  pinMode(D7, OUTPUT);

    Wire.begin(D2,D1);
      while(!bme.begin())
  {
    Serial.println("Could not find BME280 sensor!");
    delay(1000);
  }

  
  //optional code handlers to run everytime wifi is connected...
  persWM.onConnect([]() {
    DEBUG_PRINT("wifi connected");
    DEBUG_PRINT(WiFi.localIP());
    EasySSDP::begin(server);
  });
  //...or AP mode is started
  persWM.onAp([](){
    DEBUG_PRINT("AP MODE");
    DEBUG_PRINT(persWM.getApSsid());
  });

  //allows serving of files from SPIFFS
  SPIFFS.begin();
  
  // parse json config file
  File jsonFile = SPIFFS.open("/config.json", "r");
  if (jsonFile) {
    // Allocate a buffer to store contents of the file.
    size_t size = jsonFile.size();
    std::unique_ptr<char[]> jsonBuf(new char[size]);
    jsonFile.readBytes(jsonBuf.get(), size);

    DynamicJsonBuffer jsonBuffer;
    JsonObject& json = jsonBuffer.parseObject(jsonBuf.get());
    if (json.success()) {

      
      eszkozid.replace(eszkozid,json["eszkozid"]);
      ipaddr1.replace(ipaddr1,json["ipaddr1"]);
      port1 = json["port1"];
      ipaddr2.replace(ipaddr2,json["ipaddr2"]);
      port2 = json["port2"];
      refreshrate = json["refreshrate"];

    } else {
      Serial.println("failed to load json config");
    }
    jsonFile.close();
  }

  //sets network name for AP mode
  persWM.setApCredentials(DEVICE_NAME);
  //persWM.setApCredentials(DEVICE_NAME, "password"); optional password

  //make connecting/disconnecting non-blocking
  persWM.setConnectNonBlock(true);

  //in non-blocking mode, program will continue past this point without waiting
  persWM.begin();

  //handles commands from webpage, sends live data in JSON format
  server.on("/api", []() {
    DEBUG_PRINT("server.on /api");
    if (server.hasArg("x")) {
      x = server.arg("x").toInt();
      DEBUG_PRINT(String("x: ") + x);
    } //if
    if (server.hasArg("y")) {
      y = server.arg("y");
      DEBUG_PRINT("y: " + y);
    } //if
    if (server.hasArg("eszkozid")) {
      eszkozid = server.arg("eszkozid");
      saveConfig();
    } //if
    if (server.hasArg("ipaddr1")) {
      ipaddr1 = server.arg("ipaddr1");
      saveConfig();
    } //if
    if (server.hasArg("port1")) {
    port1 = server.arg("port1").toInt();
    saveConfig();
    } //if
    if (server.hasArg("ipaddr2")) {
      ipaddr2 = server.arg("ipaddr2");
      saveConfig();
    } //if
    if (server.hasArg("port2")) {
    port2 = server.arg("port2").toInt();
    saveConfig();
    } //if
    if (server.hasArg("refreshrate")) {
    refreshrate = server.arg("refreshrate").toInt();
    saveConfig();
    } //if

    
    float temp(NAN), hum(NAN), pres(NAN);

    BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
    BME280::PresUnit presUnit(BME280::PresUnit_Pa);

    bme.read(pres, temp, hum, tempUnit, presUnit);

    //build json object of program data
    StaticJsonBuffer<200> jsonBuffer;
    JsonObject &json = jsonBuffer.createObject();
    json["x"] = temp;
    json["y"] = hum;
    json["eszkozid"] = eszkozid;
    json["ipaddr1"] = ipaddr1;
    json["port1"] = port1;
    json["ipaddr2"] = ipaddr2;
    json["port2"] = port2;
    json["refreshrate"] = refreshrate;
    json["stopper"] = millis() - stopper;

    char jsonchar[200];
    json.printTo(jsonchar); //print to char array, takes more memory but sends in one piece
    server.send(200, "application/json", jsonchar);

  }); //server.on api
  

  // Set up mDNS responder:
  // - first argument is the domain name, in this example
  //   the fully-qualified domain name is "esp8266.local"
  // - second argument is the IP address to advertise
  //   we send our IP address on the WiFi network
  if (!MDNS.begin("bme280")) {
    Serial.println("Error setting up MDNS responder!");
    while(1) { 
      delay(1000);
    }
  }
  Serial.println("mDNS responder started");

  server.begin();
  stopper = millis();
  DEBUG_PRINT("setup complete.");
    
  // Add service to MDNS-SD
  MDNS.addService("http", "tcp", 80);
} //void setup  


/*=====|Save configuration to config.json|===== */
void saveConfig(){
        String newjson;
        // parse json config file
        File jsonFile = SPIFFS.open("/config.json", "r+");
        if (jsonFile) {
          // Allocate a buffer to store contents of the file.
          size_t size = jsonFile.size();
          std::unique_ptr<char[]> jsonBuf(new char[size]);
          jsonFile.readBytes(jsonBuf.get(), size);

          DynamicJsonBuffer jsonBuffer;
          JsonObject& json = jsonBuffer.parseObject(jsonBuf.get());
          if (json.success()) {
            json["eszkozid"] = eszkozid;
            json["ipaddr1"] = ipaddr1;
            json["port1"] = port1;
            json["ipaddr2"] = ipaddr2;
            json["port2"] = port2;
            json["refreshrate"] = refreshrate;
            json.printTo(newjson);
          } else {
            Serial.println("failed to load json config");
          }
          jsonFile.close();
        }
         // open file for writing
          File f = SPIFFS.open("/config.json", "w");
          if (!f) {
              Serial.println("file open failed");
          }
          Serial.println("====== Writing to SPIFFS file =========");
          // write 10 strings to file
          f.print(newjson);
          f.close();
}

/*=====|Pushing data to server|=====*/
void doRequest(String ipaddr,int port,bool startStopper){
  if ( millis() - stopper > refreshrate * 60000){
    Serial.print("|connectServer|: Kapcsolodás a hosthoz:  ");
    Serial.println(ipaddr);
    
    // Use WiFiClient class to create TCP connections
    WiFiClient client;
    if (!client.connect(ipaddr, port)) {
      Serial.println("|connectServer|: connection failed");
      if (startStopper){
        // Stopper inditasa
        Serial.println("STOPPER STARTED");
        stopper = millis();
      }
      return;
    }
    
    /* Get temp and hum */
    float temp(NAN), hum(NAN), pres(NAN);

    BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
    BME280::PresUnit presUnit(BME280::PresUnit_Pa);

    bme.read(pres, temp, hum, tempUnit, presUnit);

    // kristofg.me:5000/log/cshutohaz?homerseklet=23&paratartalom=0.5
    // We now create a URI for the request
      String url = "/log/";
      url += eszkozid;
      url += "?homerseklet=";
      url += temp;
      url += "&paratartalom=";
      url += hum;
    
    Serial.print("|connectServer|: következő kérés elküldve: ");
    Serial.println(url);
    Serial.println("|connectServer|: Válasz a szervertől: ");
    Serial.println("-------------------------------------------------");
    // This will send the request to the server
    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                "Host: " + ipaddr + "\r\n" + 
                "Connection: close\r\n\r\n");
    unsigned long timeout = millis();
    while (client.available() == 0) {
      if (millis() - timeout > 5000) {
        Serial.println(">>> Client Timeout !");
        client.stop();
        return;
      }
    }
    
    // Read all the lines of the reply from server and print them to Serial
    while(client.available()){
      String line = client.readStringUntil('\r');
      Serial.print(line);
    }
    
    Serial.println("\n-------------------------------------------------");
    Serial.println("|connectServer|: kapcsolat lezárása");
    if (startStopper){
      // Stopper inditasa
      Serial.println("STOPPER STARTED");
      stopper = millis();
    }
    
  }
}

/*=====[TCP GC]=====*/
void tcpCleanup(){
  while(tcp_tw_pcbs!=NULL)
  {
    tcp_abort(tcp_tw_pcbs);
  }
}

/* ======[RELAY CONTROL]====== */
void relay(){
  getSensorData();
  if ( 17 > tempValue || 23 < tempValue ){
      Serial.println("[ RELAYCONTROL ]: Temp alert!");
      if( tempValue < 17 && firstAlert){
        Serial.println("[ RELAYCONTROL ]: Temps below safe range.");
        digitalWrite(D5, LOW);
        delay(5000);
        digitalWrite(D5, HIGH);
        firstAlert = false;
      }
      else if( tempValue > 22 && firstAlert){
        Serial.println("[ RELAYCONTROL ]: Temps above safe range.");
        digitalWrite(D7,LOW);
        delay(5000);
        digitalWrite(D7, HIGH);
        firstAlert = false;
      }
    }
    else {
      Serial.println("[ RELAYCONTROL ]: Temps between defined safe range.");
      digitalWrite(D5,HIGH);
      digitalWrite(D7,HIGH);
      if(18 < tempValue && 22 > tempValue){
        firstAlert = true;
      }
    }
}

/* ======[GET TEMP DATA FROM SENSOR]======= */
void getSensorData(){
  float temp(NAN), hum(NAN), pres(NAN);
  BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
  BME280::PresUnit presUnit(BME280::PresUnit_Pa);
  bme.read(pres, temp, hum, tempUnit, presUnit);
  tempValue = temp;
  humValue = hum;
  Serial.print("[ SENSOR READ ]: ");
  Serial.print(tempValue);
  Serial.print(" °C");
  Serial.print(humValue);
  Serial.println(" %");
}

//* NON-BLOCKING EVENT LOOP *//
void loop() {
  
  persWM.handleWiFi();
  dnsServer.processNextRequest();
  server.handleClient();

  //* freemem *//
  tcpCleanup();

  if (refreshrate == 0) refreshrate = 1;

  //* Making request to configurable IP:PORT then starting timer (non-blocking) *//
  doRequest(ipaddr1,port1,false);
  doRequest(ipaddr2,port2,true);

  relay();
}