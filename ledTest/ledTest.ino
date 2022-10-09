const int L1 = 8;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
  pinMode(L1, OUTPUT); //Setup for LED
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(L1, HIGH);
  delay(1000);
  digitalWrite(L1, LOW);
  delay(1000);
}
