[app]
# Application basic info
title = 极简日历
package.name = calendarapk
package.domain = org.calendar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Dependencies
requirements = python3,kivy,kivymd
android.api = 33
android.ndk = 25b
android.sdk = 33
android.permissions = INTERNET
android.arch = armeabi-v7a,arm64-v8a
android.use_aapt2 = True
android.enable_androidx = True

# Appearance
# android.icon = %(source.dir)s/assets/icon.png
android.buildtools = 33.0.0
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
warn_on_root = 1