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

# Make the expect script executable
chmod +x advanced_expect.exp

# Install expect if not available
if ! command -v expect &> /dev/null; then
    echo "Installing expect..."
    apt-get update && apt-get install -y expect
fi

# Run the advanced expect script
echo "Running advanced expect script..."
expect advanced_expect.exp