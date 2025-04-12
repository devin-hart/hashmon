# 🦴 Hashmon

A lightweight, mobile-friendly hashrate monitoring app for XLA and SALV miners.

---

## 📱 Mobile (Kivy for Android)

`hashmon` runs as a native Android app using [Kivy](https://kivy.org) and [Buildozer](https://github.com/kivy/buildozer).

### Features:
- Live stats for XLA and SALV miners via Fastpool
- Progress bar countdown between refreshes
- Worker grid with names and hashrates
- Highlight highest hashrate worker per coin
- Auto-refresh every 30 seconds
- Human-readable hashrate formatting (KH/s, MH/s, GH/s, etc.)
- Touch-friendly layout

---

## ⚙️ Build Instructions

### Requirements
- Linux system (WSL or native)
- Python 3.10+
- `buildozer`, `cython`, and Android SDK/NDK tools

### Steps

1. Install Buildozer dependencies:
   ```bash
   sudo apt install -y buildozer git zip unzip openjdk-17-jdk
   pip install buildozer cython
   ```

2. Initialize:
   ```bash
   buildozer init
   ```

3. Update your `buildozer.spec` file:
   - Set the correct app name and package
   - Make sure `requirements` includes `kivy`, `requests`
   - Set the appropriate Android SDK and Python version (usually `python3` or `python3.11`)

4. Build the APK:
   ```bash
   buildozer -v android debug
   ```

5. Your signed `.apk` will be in the `bin/` directory.

---

---

## 📄 License

MIT License
