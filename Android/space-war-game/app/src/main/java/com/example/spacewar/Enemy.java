package com.example.spacewar;

import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Rect;

import static com.example.spacewar.GameView.screenX;

public class Enemy {

    public int speed = 10;
    public boolean wasShot = true;
    int x = 0;
    int y;
    int width;
    int height;
    Bitmap enemy;

    Enemy(Resources res) {

        enemy = BitmapFactory.decodeResource(res, R.drawable.enemy);

        width = enemy.getWidth();
        height=enemy.getHeight();

        float imageRatio=(float) enemy.getHeight()/enemy.getWidth(); // for maintaining original size of image

        width = screenX/4;
        height= (int) (imageRatio*width);

        enemy = Bitmap.createScaledBitmap(enemy, width, height, false);
        y = -height; //-ve for placing enemy off the screen initially
    }

    Bitmap getEnemy () {
        return enemy;
    }

    // for collision making shape of enemy
    Rect getCollisionShape () {
        return new Rect(x, y, x + width, y + height);
    }

}
