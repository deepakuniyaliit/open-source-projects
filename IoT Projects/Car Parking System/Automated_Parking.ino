#include <Servo.h>

Servo gate;              //MOTOR FOR GATE

int gate_en,gate_ex,c1,c2,c3;
int z=0;

//NOTE:- ALL THE IR SENSORS HERE, ARE ACTIVE LOW CONFIGURED.

#define GATE_PIN 7          //SERVO MOTOR WORKS HERE
#define GATE_ENTRY 2        //SENSOR FOR ENTRY
#define GATE_EXIT 3         //SENSOR FOR EXIT
#define CAR1 4
#define CAR2 5
#define CAR3 6
#define LIGHT 8

void gate_entry(){                          //servo motor opens and closes gate
    gate.write(-110);
    while(digitalRead(GATE_ENTRY)==0);
    delay(2000);
    gate.write(110);
}


void gate_exit(){                          //servo motor opens and closes gate
    gate.write(-110);
    while(digitalRead(GATE_EXIT)==0);
    delay(2000);
    gate.write(110);
}

void setup() {
    gate.attach(GATE_PIN);
    pinMode(GATE_ENTRY,INPUT);              //entry gate
    pinMode(CAR1,INPUT);                    //car1
    pinMode(CAR2,INPUT);                    //car2
    pinMode(CAR3,INPUT);                    //car3
    pinMode(GATE_EXIT,INPUT);               //exit gate
    pinMode(LIGHT,OUTPUT);                  //Red light
    Serial.begin(115200);
}

void loop(){
    gate_en=digitalRead(GATE_ENTRY);
    gate_ex=digitalRead(GATE_EXIT);
    c1=digitalRead(CAR1);
    c2=digitalRead(CAR2);
    c3=digitalRead(CAR3);
    if(gate_en==0&&(!(c1==0&&c2==0&&c3==0))){           // checks if car is there at the enty && also if parking is not full
        gate_entry();
        Serial.println("ENTRY");
    }
    /*
    COUNTER CAN BE MAINTAINED TO CHECK NO. OF CARS.
    
    if(c1==0){
        //car1 is here
        z++;
    }
    else if(c1==1)
        z--;
    if(c2==0){
        //car2 is here
        z++;
    }
    else if(c2==1)
        z--;
    if(c3==0){
        //car3 is here
        z++;
    }
    else if(c3==1)
        z--;
    */
    if(gate_ex==0&&!(c1==0&&c2==0&&c3==0)){
        gate_exit();
        Serial.println("EXIT");
    }
    if(c1==0&&c2==0&&c3==0){
        digitalWrite(LIGHT,HIGH);
        Serial.println("STOP");
    }
    else{
        digitalWrite(LIGHT,LOW);
        Serial.println("SPACE LEFT");
    }
}
