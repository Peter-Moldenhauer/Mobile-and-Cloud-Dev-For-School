package com.example.admin.androidsqliteandlocation;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    // This method is called when the 'Click Here' button is clicked
    public void buttonClicked(View view){
        Intent intent = new Intent(this, activity2.class);
        startActivity(intent);
    }
}
