package com.example.spacewar;

import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Rect;

import static com.example.spacewar.GameView.screenX;

public class Bullet {

    int x;
    int y;
    int width;
    int height;
    Bitmap bullet;

    Bullet (Resources res) {

        bullet = BitmapFactory.decodeResource(res, R.drawable.bullet);

        width = bullet.getWidth();
        height = bullet.getHeight();

        float imageRatio = (float)height / width;

        width = screenX/50;
        height = (int) (imageRatio*width);

        bullet = Bitmap.createScaledBitmap(bullet, width, height, false);

    }

    Rect getCollisionShape () {
        return new Rect(x, y, x + width, y + height);
    }

}
