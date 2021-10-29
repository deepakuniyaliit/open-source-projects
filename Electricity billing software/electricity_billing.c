#include<stdio.h>
#include<conio.h>


int main()
{
    int meter_no,customer_id;
    float unit,unit_consume,amount,rate;
    char name[30],adderess[30];

    printf("customer name:-");
    scanf("%[^\t\n]",name);
    fflush(stdin);

    printf("customer adderess:-");
    scanf("%[^\t\n]",adderess);
    fflush(stdin);

    printf("customer ID:-");
    scanf("%d",&customer_id);
    fflush(stdin);

    printf("meter no:-");
    scanf("%d",&meter_no);
    fflush(stdin);

    printf("unit consume:-");
    scanf("%f",&unit_consume);
    fflush(stdin);

    if(unit_consume<=100)
    {
        rate=5;
        amount=rate*unit_consume;
    }
    else if(unit_consume<=200)
    {
        rate=7;
        amount=500+(unit_consume-100)*7;
    }
    else if(unit_consume<=400)
    {
        rate=9;
        amount=1900+(unit_consume-200)*9;
    }
    else if(unit_consume<=700)
    {
        rate=11;
        amount=4600+(unit_consume-400)*11;
    }
    else
    {
        rate=15;
        amount=7900+(unit_consume-700)*15;
    }

    printf("\n");
    printf("\n*********************************************************************************************************************");
    printf("\n\t\t\t\t\t\tE-BILL");
    printf("\n*********************************************************************************************************************");

    printf("\ncustomer name:-%s",name);
    printf("\ncustomer adderess:-%s",adderess);
    printf("\nmeter no:-%d",meter_no);
    printf("\nunit consume:-%f",unit_consume);
    printf("\n---------------------------------------------------------------------------------------------------------------------");
    printf("\n\n rate/unit");
    printf("\n Rate<=100 is Rs.5=500");
    printf("\n Rate>100 and <=200 is Rs.7 =700");
    printf("\n Rate>200 and <=400 is Rs.9= 900");
    printf("\n Rate>400 and <=700 is Rs.11= 1100");
    printf("\n Rate>700 is Rs.15= 1500");
    printf("\n\n\t Rate/Unit is:-%.2f",rate);
    printf("\n\n\t Total Amount is:-%.2f",amount);
    

    return 0;

}
