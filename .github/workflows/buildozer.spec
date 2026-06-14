[app]
title = 9211 Automation
package.name = vaxapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,csv
version = 0.1
requirements = python3,kivy,kivymd,requests,jnius
orientation = portrait
osx.kivy_version = 2.1.0
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
