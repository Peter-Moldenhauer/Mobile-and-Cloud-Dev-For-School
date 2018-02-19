package com.example.admin.myfirstapplication;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button_hor = (Button) findViewById(R.id.horizontal);
        button_hor.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                Intent intent = new Intent(MainActivity.this, horizontal_activity.class);
                startActivity(intent);
            }
        });

        Button button_vert = (Button) findViewById(R.id.vertical);
        button_vert.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                Intent intent = new Intent(MainActivity.this, vertical_activity.class);
                startActivity(intent);
            }
        });

        Button button_grid = (Button) findViewById(R.id.grid);
        button_grid.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                Intent intent = new Intent(MainActivity.this, grid_activity.class);
                startActivity(intent);
            }
        });

        Button button_rel = (Button) findViewById(R.id.relative);
        button_rel.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                Intent intent = new Intent(MainActivity.this, relative_activity.class);
                startActivity(intent);
            }
        });
    }
}
