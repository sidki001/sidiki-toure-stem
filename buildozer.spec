[app]
title = Sidiki Toure STEM
package.name = sidikitourestem
package.domain = org.stem
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
icon.filename = icon.png
orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.minapi = 21
android.targetapi = 33
requirements = python3==3.11.0,kivy==2.1.0,android,plyer
android.allow_backup = True
fullscreen = 0
presplash.filename = presplash.png

[buildozer]
log_level = 2
build_dir = ./build
bin_dir = ./bin
android.sdk = 
android.ndk = 
android.ant = 
android.gradle = 
android.java = 
android.accept_sdk_license = True
android.ndk_version = 25b
android.sdk_version = 33

# 👇 NOUVELLE SECTION : On force une version spécifique de libffi
android.add_src =
android.gradle_repositories =
android.gradle_dependencies =
android.add_assets =
android.add_src =
android.add_java =
android.add_libs =
# Fin de la nouvelle section
