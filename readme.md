# Flashbangd version 1.1

- ✅ Full Windows compatibility
- ✅ Fully minimized tray daemon (no terminal, no window)
- ✅ Troll Quit button with fake exit + secret minigame
- ✅ Flash image appears fullscreen for 2s and disappears
- ✅ F10 global hotkey or --trigger support
- ✅ Works on Linux and Windows with tray menu
- ✅ Configurable image/sound/delay via `config.ini`
- ✅ Silent background operation (no terminal messages)

---

# 💣 Flashbangd – The Terminal Flashbang Daemon

A **devious, fullscreen flashbang simulator** for Linux and Windows, written in Python with wxPython.  
It plays a loud sound and blinds you with a fullscreen image at **random intervals**… or instantly when you press a key (F10).  
Supports **system tray**, **random delay**, **troll exit game**, and **hidden background execution**.

---

## 📦 Features

- ✅ System tray support (Windows/Linux)
- ✅ Fullscreen flash image
- ✅ Instant sound playback (no latency!)
- ✅ Random flash timing (from `45s` to `10min+`)
- ✅ Troll exit button with minigame to unlock real exit
- ✅ F10 global hotkey (X11 only) or `--trigger`
- ✅ Silent operation (no logs in terminal)
- ✅ Configurable image, sound, delay

---

## 🧰 Requirements

- Python 3.9+
- Linux (X11 or Wayland) or Windows 10/11
- Python libraries:
  ```
  pip install wxPython pygame keyboard
  ```

---

## 📁 Folder Structure

```
flashbangd/
├── flashbangd_wx.py       # main script
├── config.ini             # configuration
├── requirements.txt       # pip dependencies
└── assets/
    ├── flashbang.jpg      # your image
    └── flashbang.mp3      # your sound effect
```

---

## ⚙️ Config Guide (`config.ini`)

```ini
[settings]
delay_min = 45
delay_max = 600
image = assets/flashbang.jpg
sound = assets/flashbang.mp3
```

🧠 To adjust how often it flashbangs you:  
- Increase `delay_min` and `delay_max`

🎵 To change the flash sound:  
- Replace `assets/flashbang.mp3` with your own

🖼 To change the image:  
- Replace `assets/flashbang.jpg` with your own full-screen image

---

## 🧪 How to Run

### 🟪 Linux:
```bash
python3 flashbangd.py
```

### 🟦 Windows:
Double-click the compiled `.exe` or run with:

```bash
python flashbangd.py
```

### ⚡ Manual Trigger:
```bash
python flashbangd.py --trigger
```

### There will be a prebuilt windows .exe file here

---

## 🪟 Global Hotkey (F10)

- Works out of the box on X11 (needs `sudo`)
```bash
sudo python3 flashbangd.py
```

On Wayland: use `--trigger` from your compositor's keybind (e.g., Hyprland).

---

## 🛠 Run on Startup (Linux systemd user service)

1. Create service file:

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/flashbang.service
```

Paste:

```ini
[Unit]
Description=Flashbang Daemon

[Service]
ExecStart=/usr/bin/python3 /absolute/path/to/flashbangd.py
Restart=always

[Install]
WantedBy=default.target
```

2. Enable and start:

```bash
systemctl --user daemon-reexec
systemctl --user enable --now flashbang.service
```

---

## 🎮 Troll Quit Behavior

- Clicking "Quit" opens a fake dialog.
- If you click "Okay" → nothing happens.
- If you click "What?" → minigame with 9 tiles appears.
- Only one random tile has a big **X** to quit.
- Others show "you lost" and offer Retry or Okay.
- You can't escape easily. 😈

---

## 📜 License

BSD-3 Clause

> Do what you want. Just don’t sue me when you flashbang your boss.
