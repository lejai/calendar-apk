#!/bin/bash

# Create buildozer.spec
echo "[app]" > buildozer.spec
echo "title = CalendarApp" >> buildozer.spec
echo "package.name = calendarapk" >> buildozer.spec
echo "package.domain = org.calendar" >> buildozer.spec
echo "source.dir = ." >> buildozer.spec
echo "source.include_exts = py,png,jpg,kv,atlas" >> buildozer.spec
echo "version = 1.0.0" >> buildozer.spec
echo "requirements = python3,kivy" >> buildozer.spec
echo "android.api = 33" >> buildozer.spec
echo "android.sdk = 33" >> buildozer.spec
echo "android.ndk = 25b" >> buildozer.spec
echo "android.arch = armeabi-v7a" >> buildozer.spec
echo "android.permissions = INTERNET" >> buildozer.spec
echo "[buildozer]" >> buildozer.spec
echo "log_level = 2" >> buildozer.spec
echo "warn_on_root = 0" >> buildozer.spec

# Install expect if not already installed
apt-get update && apt-get install -y expect

# Create expect script to automatically answer the prompt
cat > answer_prompt.exp << 'EOF'
#!/usr/bin/expect -f

# Set timeout
set timeout -1

# Run buildozer
spawn buildozer android debug

# Wait for the prompt and send 'y'
expect "Are you sure you want to continue [y/n]?" {
    send "y\r"
}

# Wait for the process to finish
expect eof
EOF

chmod +x answer_prompt.exp

# Run the expect script
./answer_prompt.exp