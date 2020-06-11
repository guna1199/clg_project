#include<LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);
double rev=0;
int rpm;
int oldtime=0;
int time;

void isr() //interrupt service routine
{
rev++;
}

void setup()
{
lcd.begin();                //initialize LCD
attachInterrupt(0,isr,RISING); //attaching the interrupt
Serial.begin(9600);
}

void loop()
{
delay(6000);
detachInterrupt(0);           //detaches the interrupt
time=millis()-oldtime;        //finds the time 
rpm=(rev/time)*60000;
Serial.println(rpm);//calculates rpm
oldtime=millis();             //saves the current time
rev=0;
lcd.clear();
lcd.setCursor(0,0);
lcd.print("   TACHOMETER   ");
lcd.setCursor(0,1);
lcd.print("RPM:-  ");
lcd.print(     rpm);
lcd.print("   ");
attachInterrupt(0,isr,RISING);
}
