package com.example.mealbox;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.webkit.JavascriptInterface;
import android.view.Window;
import android.view.WindowManager;
import android.view.MotionEvent;
import android.view.View;
import android.content.res.Configuration;
import android.os.Build;
import android.os.Environment;
import android.widget.Toast;
import java.io.File;
import java.io.FileOutputStream;

public class MainActivity extends Activity {
    private WebView webView;
    private long backPressedTime = 0;
    private float startY = 0;
    private boolean isAtTop = false;

    public class WebAppInterface {
        @JavascriptInterface
        public boolean isSystemDark() {
            int nightModeFlags = getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK;
            return nightModeFlags == Configuration.UI_MODE_NIGHT_YES;
        }

        @JavascriptInterface
        public boolean saveBackupFile(String jsonContent) {
            try {
                File downloadDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
                if (!downloadDir.exists()) downloadDir.mkdirs();
                String fileName = "MealBox_Backup_" + System.currentTimeMillis() + ".json";
                File file = new File(downloadDir, fileName);
                FileOutputStream fos = new FileOutputStream(file);
                fos.write(jsonContent.getBytes("UTF-8"));
                fos.close();

                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Saved: " + fileName, Toast.LENGTH_LONG).show());
                return true;
            } catch (Exception e) {
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Save Failed: " + e.getMessage(), Toast.LENGTH_SHORT).show());
                return false;
            }
        }

        @JavascriptInterface
        public void exitApp() {
            runOnUiThread(() -> {
                if (System.currentTimeMillis() - backPressedTime < 2000) {
                    finish();
                } else {
                    backPressedTime = System.currentTimeMillis();
                    Toast.makeText(MainActivity.this, "Press back again to exit", Toast.LENGTH_SHORT).show();
                }
            });
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
        setContentView(R.layout.activity_main);

        webView = (WebView) findViewById(R.id.webview);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setLoadsImagesAutomatically(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            settings.setForceDark(WebSettings.FORCE_DARK_OFF);
        }

        webView.addJavascriptInterface(new WebAppInterface(), "AndroidTheme");
        webView.setWebChromeClient(new WebChromeClient());
        webView.setWebViewClient(new WebViewClient());

        // Intercept downward drag gesture at top of webview
        webView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        startY = event.getY();
                        isAtTop = (webView.getScrollY() <= 0);
                        break;
                    case MotionEvent.ACTION_MOVE:
                        if (isAtTop) {
                            float diffY = event.getY() - startY;
                            if (diffY > 0) {
                                webView.evaluateJavascript("if(typeof onNativePullMove === 'function'){ onNativePullMove(" + diffY + "); }", null);
                            }
                        }
                        break;
                    case MotionEvent.ACTION_UP:
                    case MotionEvent.ACTION_CANCEL:
                        if (isAtTop) {
                            float totalDiff = event.getY() - startY;
                            webView.evaluateJavascript("if(typeof onNativePullRelease === 'function'){ onNativePullRelease(" + totalDiff + "); }", null);
                        }
                        isAtTop = false;
                        startY = 0;
                        break;
                }
                return false;
            }
        });

        webView.loadUrl("file:///android_asset/index.html");
    }

    @Override
    public void onBackPressed() {
        if (webView != null) {
            webView.evaluateJavascript("if (typeof handleAppBackPress === 'function') { handleAppBackPress(); }", null);
        } else {
            super.onBackPressed();
        }
    }
}
