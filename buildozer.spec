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

# Appearance
android.icon = %(source.dir)s/assets/icon.png
android.buildtools = 33.0.0
android.apptheme = @android:style/Theme.Material.Light.NoActionBar

# Other settings
log_level = 2
warn_on_root = 1