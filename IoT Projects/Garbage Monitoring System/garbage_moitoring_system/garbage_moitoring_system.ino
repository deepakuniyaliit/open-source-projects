#include<Servo.h>
#include<ESP8266WiFi.h>
#include<BlynkSimpleEsp8266.h>
#include<FirebaseArduino.h>

char blynk_auth[] = "AawWDIkxreCFbwppLjqLMiEW-0xvaY5l";             // Blynk_Auth_Token

const char *ssid =  "Get_ur_own_WiFi";                            // replace with your wifi ssid and wpa2 key
const char *pass =  "mai_ni_batara";

#define FIREBASE_HOST "smart-dustbin-296ba-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "Xow2gaZJTWBDg2CzToo838Yn0gDnoQvulsM5zVIn"

Servo s;

int z=0,t=0,k=-1;

// With V0, the vertical bar is connected
WidgetLCD lcd(V1);
WidgetTerminal terminal(V2);

void setup() 
{
      Serial.begin(9600);
      delay(10);

      pinMode(D0,INPUT);        //outside sensor
      pinMode(D1,INPUT);        //inside sensor (100%)
      pinMode(D4,INPUT);        //inside sensor (50%)
      pinMode(D3,INPUT);        //inside sensor (25%)
      s.attach(D2);             //Servo motor

      Serial.println("");
      Serial.println("Connecting to ");
      Serial.println(ssid);
 
      WiFi.begin(ssid, pass);
 
      while (WiFi.status() != WL_CONNECTED){
            delay(500);
            Serial.print(".");
      }

      Serial.println("");
      Serial.println("WiFi connected");

      Serial.println("");
      Serial.println("Connecting to Firebase.. ");
      
      //firebase connection
      Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
      if(Firebase.failed())
          Serial.print(Firebase.error());
      else{
          Serial.print("Firebase Connected");
          Firebase.setInt("Level-of-Bin/Value",0);
      }

      String s2=Firebase.getString("Active");
      if(Firebase.success()){
          Serial.println("\nStatus of Device:");
          Serial.print(s2);
      }
      else
          Serial.println("Device not connected to database");

      Blynk.begin(blynk_auth,ssid,pass);
      Blynk.notify("NODEMCU Online");
      Blynk.email("kbandooni1@gmail.com", "NODEMCU Online");                                                      

      // Dustbin ON
      lcd.clear();
      lcd.print(4,0,"DUSTBIN");
      lcd.print(3,1,"CONNECTED");
      
      //Dustbin Initially empty
      t=0;

      //Dustbin Vertical Fill Empty initially
      Blynk.virtualWrite(V0,t);
      
      //blynk lcd
      delay(4000);
      lcd.clear();
}

void loop() 
{
      Blynk.run();                                                              // Blynk magic 
      
      terminal.println("\n");
      terminal.print("Dustbin Status: ");
      terminal.print(t);
      terminal.println("%");

      Blynk.virtualWrite(V0,t);
      
      if(!digitalRead(D0)){
           s.write(10);        //servo motor opens the lid of dustbin
           while(!digitalRead(D0)){
               delay(2000);
           }
           s.write(90);       //servo motor closes lid of dustbin
      }

      if(!digitalRead(D1) && k!=3){                                    //dustbin at 80%
           lcd.clear();
           lcd.print(2,0,"DUSTBIN FULL");
           lcd.print(3,1,"EMPTY IT");
           //notify whatever you want to...
           Blynk.notify("Dustbin Full, Empty it!! :)"); 
           Blynk.email("kbandooni1@gmail.com","Dustbin Full, Empty it!! :)");
           k=3;
           t=80;
           Firebase.setInt("/Level-of-Bin/Value",t);
           if(Firebase.failed())
               Serial.print(Firebase.error());
           else
               Serial.println("Value Sent");
      }
 
      if(!digitalRead(D4) && k!=2 && digitalRead(D1)==1){                //dustbin at 50%
           lcd.clear();
           lcd.print(4,0,"DUSTBIN:");
           lcd.print(3,1,"HALF-FULL");
           k=2;
           t=50;
           Firebase.setInt("/Level-of-Bin/Value",t);
           if(Firebase.failed())
                Serial.print(Firebase.error());
           else
                Serial.println("Value Sent");
      }

      if(!digitalRead(D3) && k!=1 && digitalRead(D4)==1){                //dustbin at 25%
           lcd.clear();
           lcd.print(4,0,"DUSTBIN:");
           lcd.print(5,1,"AT 25%");
           k=1;
           t=25;
           Firebase.setInt("/Level-of-Bin/Value",t);
           if(Firebase.failed())
               Serial.print(Firebase.error());
           else
               Serial.println("Value Sent");
      }
 
      if(k!=0 && digitalRead(D1)==1 && digitalRead(D3)==1 && digitalRead(D4)==1){
           k=0;
           t=0;
           Firebase.setInt("/Level-of-Bin/Value",t);
           if(Firebase.failed())
                Serial.print(Firebase.error());
           else
                Serial.println("Value Sent");
           lcd.clear();
           lcd.print(1,0,"DUSTBIN LEVEL:");
           lcd.print(4,1,"EMPTY :D");
      }
}
