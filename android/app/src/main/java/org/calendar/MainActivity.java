
package org.calendar;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // 初始化 Python
        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        
        // 运行 Python 代码
        Python py = Python.getInstance();
        PyObject pyObject = py.getModule("main");
        pyObject.callAttr("run_app");
    }
}

