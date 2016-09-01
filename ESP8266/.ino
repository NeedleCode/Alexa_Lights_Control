/*
 *  This sketch demonstrates how to set up a simple HTTP-like server.
 *  The server will set a GPIO pin depending on the request
 *    http://server_ip/gpio/0 will set the GPIO2 low,
 *    http://server_ip/gpio/1 will set the GPIO2 high
 *  server_ip is the IP address of the ESP8266 module, will be 
 *  printed to Serial when the module is connected.
 */

 /*This cod came with the esp8266 arduino examples We just modify some parameters an add
 little specif changes*/

#include <ESP8266WiFi.h>
#include <string.h>

const char* ssid = "TP-LINK";
const char* password = "";
const int analogOutPin = 12;
const int pwmFrecuency=5000;
const int timeout=10;

// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  delay(10);
//

  // prepare GPIO2
 // pinMode(2, OUTPUT);
 // analogWrite(2, 0);
  //Set pwm frecuency
  analogWriteFreq(pwmFrecuency);
  
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

 //setting Ip of device
  
  WiFi.begin(ssid, password);
  
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);    
    Serial.print(".");
   
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.println(WiFi.localIP());
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
     //Serial.println("Client not founded");
    return;
  }
  
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
  
  // Read the first line of the request
  String req = client.readStringUntil('/n');
  Serial.println(req);
  client.flush();
  
  // Match the request
  int index1;
  int index2;
  String pwmVal="";
  if (req.indexOf("/pwm?=") != -1)
  { index1=req.indexOf("?=");
    index2=req.indexOf("HTTP");
   pwmVal=req.substring(index1+2,index2-1);    
   Serial.println(index1);
   Serial.println(index2);
   analogWrite(analogOutPin,pwmVal.toInt());
  }
  else {
    Serial.println("invalid request");
    client.stop();
    return;
  }

  // Set GPIO2 according to the request
  //digitalWrite(2, val);
  
  client.flush();

  // Prepare the response
  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n<html>\r\nPMW value is ";
  s += pwmVal;
  s += "</html>\n";

  // Send the response to the client
  client.println(pwmVal.toInt());
  delay(1);
  Serial.println("Client disonnected");

  // The client will actually be disconnected 
  // when the function returns and 'client' object is detroyed
}

