/*  PulseSensor™ Starter Project   http://www.pulsesensor.com
 *   
This an Arduino project. It's Best Way to Get Started with your PulseSensor™ & Arduino. 
-------------------------------------------------------------
1) This shows a live human Heartbeat Pulse. 
2) Live visualization in Arduino's Cool "Serial Plotter".
3) Blink an LED on each Heartbeat.
4) This is the direct Pulse Sensor's Signal.  
5) A great first-step in troubleshooting your circuit and connections. 
6) "Human-readable" code that is newbie friendly." 
*/


//  Variables
int PulseSensorPurplePin0 = 0;        // Pulse Sensor PURPLE WIRE connected to ANALOG PIN 0
int PulseSensorPurplePin1 = 1;
int PulseSensorPurplePin2 = 2;
int electroPin = 3;
const int L1 = 8;


int Signal0;                // holds the incoming raw data. Signal value can range from 0-1024
int Signal1;
int Signal2;
int SignalElec;
long temps;
long tempsPrint;


// The SetUp Function:
void setup() {
   Serial.begin(9600);         // Set's up Serial Communication at certain speed.
   
  pinMode(10, INPUT); // Setup for leads off detection LO +
  pinMode(11, INPUT); // Setup for leads off detection LO - 
  pinMode(L1, OUTPUT); //Setup for LED
   
}

// The Main Loop Function
void loop() {
  temps = millis();
  //Serial.println(temps);
  Signal0 = analogRead(PulseSensorPurplePin0);  // Read the PulseSensor's value. 
  //Serial.println((millis()-temps));
  Signal1 = analogRead(PulseSensorPurplePin1);                                            // Assign this value to the "Signal" variable.
  Signal2 = analogRead(PulseSensorPurplePin2);
  SignalElec = analogRead(electroPin);
  //Serial.println((millis()-temps)); 
  
 // Serial.print(temps);
 // Serial.print(",");
  Serial.print(Signal0);                    // Send the Signal value to Serial Plotter.
  Serial.print(",");
  Serial.print(Signal1);
  Serial.print(",");
  Serial.print(Signal2);
  Serial.print(",");
  Serial.println(SignalElec);
 // Serial.println(temps);
//Serial.println();
  if(Signal0 >= 650){
    digitalWrite(L1, HIGH);
  }
  else{
    digitalWrite(L1, LOW);  
  }
  delay(33/*-(millis()-temps)*/);
}
