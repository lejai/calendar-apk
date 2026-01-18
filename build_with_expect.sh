#!/bin/bash

# Create buildozer.spec
cat > buildozer.spec << 'EOF'
[app]
title = CalendarApp
package.name = calendarapk
package.domain = org.calendar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
android.api = 33
android.sdk = 33
android.ndk = 25b
android.arch = armeabi-v7a
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 0
EOF

# Create a simple expect script
cat > answer_prompt.exp << 'EOF'
#!/usr/bin/expect -f
spawn buildozer android debug
expect "Are you sure you want to continue [y/n]?" {send "y\r"}
expect eof
EOF

chmod +x answer_prompt.exp

# Run with expect
which expect || apt-get update && apt-get install -y expect
expect answer_prompt.exp