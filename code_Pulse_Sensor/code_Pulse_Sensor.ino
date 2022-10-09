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
int PulseSensorPurplePin0 = 0;        // Pulse Sensor PURPLE WIRE connected to ANALOG PIN
int PulseSensorPurplePin1 = 1;
int PulseSensorPurplePin2 = 2;
const int L1 = 2;                     // define PIN for LED


int Signal0;                // holds the incoming raw data. Signal value can range from 0-1024
int Signal1;
int Signal2;
long temps;
int x = 0;


// The SetUp Function:
void setup() {
   Serial.begin(9600);       // Set's up Serial Communication at certain speed. 
   pinMode(L1, OUTPUT); //Setup for LED
   
}

// The Main Loop Function
void loop() {
    temps = millis();
    if(x == 0 && temps >= 2000){      //switch on LED at 2000 ms or 2s 
      digitalWrite(L1, HIGH);
      x = 1;
      
    }
    if(x == 1 && temps >= 2100){      //switch off LED at 2100 ms or 2,1s
      digitalWrite(L1, LOW);
      x = 2;
    }
    
    Signal0 = analogRead(PulseSensorPurplePin0);  // Read the PulseSensor's value. 
    
    Signal1 = analogRead(PulseSensorPurplePin1);  // Assign this value to the "Signal" variable.
    /*Signal2 = analogRead(PulseSensorPurplePin2);
    
    Serial.print(temps);
    Serial.print(",");
    */
    Serial.println(Signal0); 
    /*// Send the Signal value to Serial Plotter.
    Serial.print(",");
    Serial.println(Signal1);
    Serial.print(",");
    Serial.println(Signal2);*/

    delay(33-(millis()-temps));               // wait 33 ms - time to take and send mesure of sensor
}
