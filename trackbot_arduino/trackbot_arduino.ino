/*
 UDPSendReceiveString:
 This sketch receives UDP message strings, prints them to the serial port
 and sends an "acknowledge" string back to the sender

 A Processing sketch is included at the end of file that can be used to send
 and received messages for testing with a computer.

 created 21 Aug 2010
 by Michael Margolis

 This code is in the public domain.
 */


#include <SPI.h>         // needed for Arduino versions later than 0018
#include <Ethernet.h>
#include <EthernetUdp.h>         // UDP library from: bjoern@cs.stanford.edu 12/30/2008
#include <Stepper.h>


// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
IPAddress ip(192, 168, 0, 51);

unsigned int localPort = 8888;      // local port to listen on

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];  //buffer to hold incoming packet,
char  ReplyBuffer[] = "acknowledged";       // a string to send back

// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

String packetBuffer_s;
int xDelta = 0;
int yDelta = 0;
const int stepsPerRevolution = 200;   // Change this to fit the stepper used
Stepper xStepper(stepsPerRevolution, 8, 9, 10, 11);   // Change pins accordingly

void setup() {
  // start the Ethernet and UDP:
  Ethernet.begin(mac, ip);
  Udp.begin(localPort);

  Serial.begin(9600);

  // Set stepper motor RPM
  xStepper.setSpeed(50);
}




void loop() {

//  // if there's data available, read a packet
//  int packetSize = Udp.parsePacket();
//  if (packetSize) {
//    Serial.print("Received packet of size ");
//    Serial.println(packetSize);
//    Serial.print("From ");
//    IPAddress remoteIp = Udp.remoteIP();
//    Serial.print(remoteIp);
//    Serial.print(", port ");
//    Serial.println(Udp.remotePort());
//
//    // read the packet into packetBufffer
//    int len = Udp.read(packetBuffer, 255);
//    if (len > 0) {
//      packetBuffer[len] = 0;
//    }
//    Serial.println("Contents:");
//    Serial.println(packetBuffer);
//
//    // Set xDelta and yDelta from the received packet data
//    int div = 0;
//    for (int i = 0; i <= 255; i++) {
//      if (packetBuffer[i] == ',') {
//        div = i;
//        break;
//      }
//    }    
//    packetBuffer_s = String(packetBuffer);
//    xDelta = packetBuffer_s.substring(0, div).toInt();
//    yDelta = packetBuffer_s.substring(div).toInt();
//
//    // Send commands to the motor accordingly to xDelta and yDelta
//    if (xDelta > 0) {
//      xStepper.step(1);
//    } else if (xDelta < 0) {
//      xStepper.step(-1);
//    }
//
//    
//    // send a reply, to the IP address and port that sent us the packet we received
//    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
//    Udp.write(ReplyBuffer);
//    Udp.endPacket();
//  }

  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.println("");
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remote = Udp.remoteIP();
    for (int i = 0; i < 4; i++) {
      Serial.print(remote[i], DEC);
      if (i < 3) {
        Serial.print(".");
      }
    }
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read the packet into packetBufffer
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    Serial.println("Contents:");
    Serial.println(packetBuffer);

    // Set xDelta and yDelta from the received packet data
    int div = 0;
    for (int i = 0; i <= 255; i++) {
      if (packetBuffer[i] == ',') {
        div = i;
        break;
      }
    }    
    packetBuffer_s = String(packetBuffer);
    xDelta = packetBuffer_s.substring(0, div).toInt();
    Serial.println("xDelta: ");
    Serial.println(xDelta);
    yDelta = packetBuffer_s.substring(div).toInt();
    Serial.println("yDelta: ");
    Serial.println(yDelta);

    // Send commands to the motor accordingly to xDelta and yDelta
    if (xDelta > 0) {
      xStepper.step(1);
    } else if (xDelta < 0) {
      xStepper.step(-1);
    }

    // send a reply to the IP address and port that sent us the packet we received
    Udp.beginPacket(Udp.remoteIP(), 8888);
    Udp.write(ReplyBuffer);
    Udp.endPacket();
  }
  delay(10);  
}

