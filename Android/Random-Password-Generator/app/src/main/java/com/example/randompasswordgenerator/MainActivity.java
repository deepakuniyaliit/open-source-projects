package com.example.randompasswordgenerator;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;

import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Random;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        AppCompatButton btGeneratePassword = findViewById(R.id.generatePasswordButton);
        AppCompatButton btCopyPassword = findViewById(R.id.copyButton);
        TextView tvPasswordOutput = findViewById(R.id.outputPassword);

        // initially hide copy button and sample password
        btCopyPassword.setVisibility(View.INVISIBLE);
        tvPasswordOutput.setVisibility(View.INVISIBLE);

        // on clicking generate button
        btGeneratePassword.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String password = getPassword();
                tvPasswordOutput.setText(password);
                // make password and copy button visible
                tvPasswordOutput.setVisibility(View.VISIBLE);
                btCopyPassword.setVisibility(View.VISIBLE);
            }
        });

        // on clicking copy button
        btCopyPassword.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // clipboardManager to store password
                ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                String data = tvPasswordOutput.getText().toString();
                ClipData temp = ClipData.newPlainText("pswd", data);
                clipboard.setPrimaryClip(temp);
                Toast.makeText(MainActivity.this, "Copied!!!", Toast.LENGTH_SHORT).show();
            }
        });


    }

    /**
     * function to generate password
     * @return password (String)
     */
    String getPassword(){
        String NUMBERS = "0123456789";
        String UPPER_ALPHABETS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        String LOWER_ALPHABETS = "abcdefghijklmnopqrstuvwxyz";
        String SPECIAL_CHARACTERS = "@#$%&*";

        String[] symbol = {NUMBERS, UPPER_ALPHABETS, LOWER_ALPHABETS, SPECIAL_CHARACTERS};
        final Random random = new Random();
        // get random password length 14-20
        int passwordLength = 14 + random.nextInt(7);
        final StringBuilder sb = new StringBuilder(passwordLength);
        for(int i = 0; i < passwordLength; i++){
            int charTypeIndex = random.nextInt(4);
            int len = symbol[charTypeIndex].length();
            sb.append(symbol[charTypeIndex].charAt(random.nextInt(len)));
        }
        return sb.toString();
    }
}