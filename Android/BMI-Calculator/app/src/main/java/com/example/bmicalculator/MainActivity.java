package com.example.bmicalculator;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    EditText etHeight, etWeight;
    AppCompatButton calculate;
    TextView tvOutput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        etHeight = findViewById(R.id.height);
        etWeight = findViewById(R.id.weight);
        tvOutput = findViewById(R.id.output);
        calculate = findViewById(R.id.calculate);

        calculate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    double height = Double.parseDouble(etHeight.getText().toString()) / 100;
                    double weight = Double.parseDouble(etWeight.getText().toString());
                    double bmi = weight/(height*height);

                    String category;
                    if(bmi <= 18.5)
                        category = "Under Weight";
                    else if(bmi <= 24.9)
                        category = "Normal Weight";
                    else if(bmi <= 29.9)
                        category = "Over Weight";
                    else
                        category = "Obesity";

                    //display on screen
                    String finalOutPut = String.format("Your BMI is : %.02f \n %s", bmi, category);
                    tvOutput.setText(finalOutPut);
                }
                catch (Exception e){
                    Toast.makeText(MainActivity.this, "Enter both details", Toast.LENGTH_SHORT).show();
                }


            }
        });
    }
}