package com.example.spacewar;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.media.AudioAttributes;
import android.media.AudioManager;
import android.media.SoundPool;
import android.os.Build;
import android.view.MotionEvent;
import android.view.SurfaceView;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class GameView extends SurfaceView implements Runnable {

    private Thread thread;
    private boolean isPlaying, isGameOver = false;
    public static int screenX, screenY;
    private int score = 0;
    public static float screenRatioX, screenRatioY;
    private Paint paint;
    private Enemy[] enemies;
    private SharedPreferences prefs;
    private Random random;
    private SoundPool soundPool;
    private List<Bullet> bullets;
    private int sound;
    private Player player;
    private GameActivity activity;
    private Background background1, background2;

    public GameView(GameActivity activity, int screenX, int screenY) {
        super(activity);

        this.activity = activity;

        prefs = activity.getSharedPreferences("game", Context.MODE_PRIVATE);


        /*
        * for sound effects
        * */
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {

            AudioAttributes audioAttributes = new AudioAttributes.Builder()
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .setUsage(AudioAttributes.USAGE_GAME)
                    .build();

            soundPool = new SoundPool.Builder()
                    .setAudioAttributes(audioAttributes)
                    .build();

        } else
            soundPool = new SoundPool(1, AudioManager.STREAM_MUSIC, 0);

        sound = soundPool.load(activity, R.raw.shoot, 1);

        /*
        * for taking screen size
        * */
        this.screenX = screenX;
        this.screenY = screenY;
        screenRatioX = 1080f / screenX;
        screenRatioY = 1920f / screenY;

        background1 = new Background(screenX, screenY, getResources());
        background2 = new Background(screenX, screenY, getResources());
        background2.y = -background2.background.getHeight();

        player = new Player(this, screenX, screenY, getResources());

        bullets = new ArrayList<>();



        paint = new Paint();
        paint.setTextSize(128);
        paint.setColor(Color.WHITE);

        enemies = new Enemy[4]; // for creating 4 enemies at a time on screen

        for (int i = 0;i < 4;i++) {

            Enemy enemy = new Enemy(getResources());
            enemies[i] = enemy;

        }

        random = new Random();

    }

    @Override
    public void run() {

        while (isPlaying) {

            update ();
            draw ();
            sleep ();

        }

    }

    private void update () {

        /*
        * for moving background up to down
        *
        * */
        background1.y += 100 * screenRatioY;
        background2.y += 100 * screenRatioY;

        /*
        * for creating loop of background
        * */
        if (background1.y > screenY) {
            background1.y = -background1.background.getHeight();
        }

        if (background2.y > screenY) {
            background2.y = -background2.background.getHeight();
        }

        /*
        * for updating player position (moving effect)
        * */
        if (player.move=='l')
            player.x -= 30 * screenRatioX;
        else if(player.move=='r')
            player.x += 30 * screenRatioX;

        //for edges so that player will not move outside the screen
        if (player.x < 0)
            player.x = 0;

        if (player.x >= screenX - player.width)
            player.x = screenX - player.width;


        /*
        * for updating bullets
        * */

        List<Bullet> trash = new ArrayList<>();

        /*
        * when bullet hit the enemy
        * */
        for (Bullet bullet : bullets) {

            if (bullet.y < 0)
                trash.add(bullet);

            bullet.y -= 50 * screenRatioY; // to move bullet up

            for (Enemy enemy : enemies) {

                //collision
                if (Rect.intersects(enemy.getCollisionShape(),
                        bullet.getCollisionShape())) {

                    score++;
                    //for removing the enemy and bullets from the screen
                    enemy.y = screenY;
                    bullet.y = -500;
                    enemy.wasShot = true;

                }

            }

        }

        for (Bullet bullet : trash)
            bullets.remove(bullet);

        /*
        * for making enemy to move
        * */
        for (Enemy enemy : enemies) {

            enemy.y += enemy.speed; // for making enemy move toward player

            //when enemy moved at the end side of player then we will add more enemies
            if (enemy.y + enemy.height >screenY) {

                int bound = (int) (30 * screenRatioY);
                enemy.speed = random.nextInt(bound); //to give random speed to enemy

                if (enemy.speed < 10 * screenRatioY) // for minimum speed
                    enemy.speed = (int) (10 * screenRatioY);

                // for placing new enemy
                enemy.y = 0;
                enemy.x = random.nextInt(screenX - enemy.width);

                enemy.wasShot = false;
            }

            /*
            * when collision take place b/w enemy and player
            * */
            if (Rect.intersects(enemy.getCollisionShape(), player.getCollisionShape())) {

                isGameOver = true;
                return;
            }

        }

    }

    private void draw () {

        if (getHolder().getSurface().isValid()) {

            Canvas canvas = getHolder().lockCanvas();
            /*
            * for showing background on screen
            * */
            canvas.drawBitmap(background1.background, background1.x, background1.y, paint);
            canvas.drawBitmap(background2.background, background2.x, background2.y, paint);

            /*
            * for drawing enemies on screen
            * */
            for (Enemy enemy : enemies)
                canvas.drawBitmap(enemy.getEnemy(), enemy.x, enemy.y, paint);

            /*
            * for drawing scores
            * */
            canvas.drawText(score + "", screenX / 2f, 164, paint);

            /*
            * for game over condition
            * */
            if (isGameOver) {
                isPlaying = false;
                canvas.drawBitmap(player.getDead(), player.x, player.y, paint); // for dead state of player

                /*
                * for displaying game over image
                * */
                Bitmap g = BitmapFactory.decodeResource(getResources(),R.drawable.game_over_logo);
                canvas.drawBitmap(g,0, 0,paint);

                getHolder().unlockCanvasAndPost(canvas);
                saveIfHighScore();
                waitBeforeExiting ();
                return;
            }

            /*
            * for making player on screen with co-ordinates
            * */
            canvas.drawBitmap(player.getPlayer(), player.x, player.y, paint);

            /*
            * for making bullets with co-ordinates
            * */
            for (Bullet bullet : bullets)
                canvas.drawBitmap(bullet.bullet, bullet.x, bullet.y, paint);

            getHolder().unlockCanvasAndPost(canvas);

        }

    }

    private void waitBeforeExiting() {

        try {
            Thread.sleep(3000);
            activity.startActivity(new Intent(activity, MainActivity.class));
            activity.finish();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }

    private void saveIfHighScore() {

        if (prefs.getInt("highscore", 0) < score) {
            SharedPreferences.Editor editor = prefs.edit();
            editor.putInt("highscore", score);
            editor.apply();
        }

    }

    private void sleep () {
        try {
            Thread.sleep(17);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void resume () {

        isPlaying = true;
        thread = new Thread(this);
        thread.start();

    }

    public void pause () {

        try {
            isPlaying = false;
            thread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }

    /*
    * when player touch screen
    * */
    @Override
    public boolean onTouchEvent(MotionEvent event) {

        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:   //when user touch the screen
                if (event.getX() < screenX / 3) { /*when user touch left side of the screen*/
                    player.move = 'l';
                }
                else if(event.getX() > 2*(screenX / 3)){   /*when user touch right side of the screen*/
                    player.move = 'r';
                }
                break;
            case MotionEvent.ACTION_UP: // when user is not touching
                player.move = ' ';
                break;
        }
        player.toShoot = true;
        return true;
    }

    public void newBullet() {

        /*
        * for bullet sound
        * */
        if (!prefs.getBoolean("isMute", false))
            soundPool.play(sound, 1, 1, 0, 0, 1);

        Bullet bullet = new Bullet(getResources());
        /*
        * setting initial co-ordinates of bullets
        * */
        bullet.x = (int) (player.x + player.width/2-(bullet.width/2));
        bullet.y = player.y;
        bullets.add(bullet);

    }

}
