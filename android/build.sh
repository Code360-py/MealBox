#!/data/data/com.termux/files/usr/bin/bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

mkdir -p build/compiled_res build/gen build/obj build/apk lib

# Ensure android.jar exists
if [ ! -f "lib/android.jar" ]; then
  if [ -f "$HOME/MealBoxApp/lib/android.jar" ]; then
    cp "$HOME/MealBoxApp/lib/android.jar" lib/android.jar
  else
    wget -q -O lib/android.jar "https://github.com/Sable/android-platforms/raw/master/android-30/android.jar"
  fi
fi

# Clean prior builds
rm -rf build/obj/* build/apk/* MealBox.apk MealBox.apk.idsig

# Compile resources & package
aapt2 compile --dir res -o build/compiled_res/
aapt2 link -I lib/android.jar \
    --manifest AndroidManifest.xml \
    -A assets \
    --java build/gen \
    -o build/apk/unaligned.apk \
    build/compiled_res/*.flat \
    --auto-add-overlay

# Compile Java
javac -cp "lib/android.jar:build/gen" \
    -d build/obj \
    build/gen/com/example/mealbox/R.java \
    src/com/example/mealbox/MainActivity.java

# Convert to DEX
d8 --lib lib/android.jar \
    --output build/apk/ \
    build/obj/com/example/mealbox/*.class

(cd build/apk && zip -u unaligned.apk classes.dex)

# Align & sign
zipalign -f -v 4 build/apk/unaligned.apk build/apk/aligned.apk

if [ ! -f "debug.keystore" ]; then
  keytool -genkey -v -keystore debug.keystore \
      -storepass android -alias androiddebugkey -keypass android \
      -keyalg RSA -keysize 2048 -validity 10000 \
      -dname "CN=MealBox,O=MealBox,C=US"
fi

apksigner sign --ks debug.keystore \
    --ks-pass pass:android \
    --ks-key-alias androiddebugkey \
    --key-pass pass:android \
    --out MealBox.apk \
    build/apk/aligned.apk

# Copy to public Downloads
termux-setup-storage
cp MealBox.apk /sdcard/Download/MealBox.apk

echo "Build successful! APK ready at: ~/MealBox/android/MealBox.apk & /sdcard/Download/MealBox.apk"
