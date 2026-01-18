[app]
# Application basic info
title = 极简日历
package.name = calendarapk
package.domain = org.calendar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Dependencies
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow==9.5.0,openssl==3.0.9
android.api = 34
android.ndk = 25b
android.sdk = 34
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.archs = arm64-v8a,armeabi-v7a
android.use_aapt2 = True
android.enable_androidx = True
android.minapi = 28
android.targetapi = 34
android.buildtools = 34.0.0

# Appearance
# android.icon = %(source.dir)s/assets/icon.png
android.apptheme = @android:style/Theme.Material.Light.NoActionBar

# Android Studio settings
android.gradle_dependencies = 
    androidx.appcompat:appcompat:1.4.1
    com.google.android.material:material:1.5.0

# Other settings
log_level = 2
warn_on_root = 0

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0