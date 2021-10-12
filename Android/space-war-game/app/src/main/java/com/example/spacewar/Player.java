package com.example.spacewar;

import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Rect;

public class Player {

    boolean toShoot = false;
    char move;
    int x;
    int y;
    int width;
    int height;
    Bitmap player, dead;
    private GameView gameView;

    Player(GameView gameView, int screenX, int screenY, Resources res) {

        this.gameView = gameView;

        player = BitmapFactory.decodeResource(res, R.drawable.player);

        float imageRatio=(float) player.getHeight()/player.getWidth(); // for maintaining original size of image
        width = screenX/5;
        height= (int)(imageRatio*width);

        player = Bitmap.createScaledBitmap(player, width, height, false);

        dead = BitmapFactory.decodeResource(res, R.drawable.dead);
        dead = Bitmap.createScaledBitmap(dead, width, height, false);

        // for co-ordinates of player
        x = screenX/2;
        y = screenY - height;

    }

    Bitmap getPlayer () {

        if (toShoot) {
            toShoot = false;
            gameView.newBullet();
        }
        return player;
    }

    Rect getCollisionShape () {
        return new Rect(x, y, x + width, y + height);
    }

    // for returning dead state
    Bitmap getDead () {
        return dead;
    }
}
