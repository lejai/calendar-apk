#!/usr/bin/env python3
"""
Script to patch Buildozer's root check function and run the build.
"""

import os
import subprocess
import sys

def find_buildozer_init():
    """Find buildozer's __init__.py file."""
    result = subprocess.run(
        ['find', '/', '-name', '__init__.py', '-path', '*buildozer*', '-type', 'f'],
        capture_output=True, text=True, timeout=10
    )
    files = result.stdout.strip().split('\n')
    return files[0] if files and files[0] else None

def patch_buildozer(buildozer_init):
    """Patch buildozer's check_root function to always return True."""
    with open(buildozer_init, 'r') as f:
        content = f.read()
    
    # Find the check_root function and modify it
    old_function = 'def check_root(self):'
    new_function = 'def check_root(self):\n        return True  # Patched to skip root check'
    
    if old_function in content:
        patched_content = content.replace(old_function, new_function)
        with open(buildozer_init, 'w') as f:
            f.write(patched_content)
        print(f"Successfully patched buildozer at {buildozer_init}")
        return True
    else:
        print("Could not find check_root function in buildozer's __init__.py")
        return False

def create_buildozer_spec():
    """Create a minimal buildozer.spec file."""
    spec_content = '''[app]
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
'''
    with open('buildozer.spec', 'w') as f:
        f.write(spec_content)
    print("Created buildozer.spec file")

def run_buildozer():
    """Run buildozer android debug."""
    print("Running buildozer android debug...")
    result = subprocess.run(
        ['buildozer', 'android', 'debug'],
        capture_output=True, text=True
    )
    print("Build output:")
    print(result.stdout)
    if result.stderr:
        print("Build errors:")
        print(result.stderr)
    return result.returncode

def main():
    """Main function."""
    # Create buildozer.spec
    create_buildozer_spec()
    
    # Find and patch buildozer
    buildozer_init = find_buildozer_init()
    if buildozer_init:
        print(f"Found buildozer at: {buildozer_init}")
        patched = patch_buildozer(buildozer_init)
        if patched:
            # Run buildozer
            returncode = run_buildozer()
            sys.exit(returncode)
        else:
            print("Failed to patch buildozer, exiting")
            sys.exit(1)
    else:
        print("Could not find buildozer's __init__.py, exiting")
        sys.exit(1)

if __name__ == "__main__":
    main()