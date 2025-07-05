# Flashbangd version 1.0.1:
- added experimental windows compatibility (might have bugs/issues)
- added minimizing to taskbar tray (no window, just working and inside the tray)

# Flashbangd version 1.0.2 sneak-peek:
- i will make it faster by probably making it into c++ or any other language faster than python (50/50 chance)
- better compatibility for wayland

## rest of readme

## |
## |
## |
## v

# 💣 Flashbangd – The Terminal Flashbang Daemon

A **devious, fullscreen flashbang simulator** for Linux, written in Python with PyQt6.  
It plays a loud sound and blinds you with a fullscreen image at **random intervals**… or instantly when you press a key (F10).  
Supports **multi-monitor**, **zero-latency audio**, and **runs hidden in the background**.

---

## 📦 Features

- ✅ Multi-monitor fullscreen support  
- ✅ Flashbang image with fade-out effect  
- ✅ Instant sound playback (no latency!)  
- ✅ Random flash timing (from `45s` to `10min+`)  
- ✅ X11 global hotkey (F10) support  
- ✅ Wayland support via `--trigger` mode (bind with Hyprland)  
- ✅ Background execution via `nohup` or `systemd --user`  
- ✅ Configurable image, sound, timing, and hotkey  

---

## 🧰 Requirements

- Python 3.9+
- Linux (X11 or Wayland)
- `mpv` (optional legacy fallback, not used now)
- Python libraries:
  ```
  pip install PyQt6 keyboard pygame
  ```

> ⚠️ On **X11**, global hotkey detection requires `sudo` for `keyboard` to work:
```bash
sudo python3 flashbang.py
```

> 🟡 On **Wayland**, hotkeys are blocked. Use Hyprland keybinds with `--trigger` (see below).

---

## 📁 Folder Structure

```
flashbangd/
├── flashbang.py          # main script
├── config.ini            # configuration
├── requirements.txt      # pip dependencies
└── assets/
    ├── flashbang.jpg     # your image
    └── flashbang.mp3     # your sound effect
```

---

## ⚙️ Config Guide (`config.ini`)

```ini
[settings]
delay_min = 45            # Minimum delay between flashes (in seconds)
delay_max = 600           # Maximum delay between flashes (in seconds)
image = assets/flashbang.jpg     # Image path
sound = assets/flashbang.mp3     # Sound path
fullscreen = true
multi_monitor = true
test_key = F10
```

🧠 To adjust how often it flashbangs you:  
- Increase `delay_min` and `delay_max`

🎵 To change the flash sound:  
- Replace `assets/flashbang.mp3` with your own  
- Keep it short and punchy for best effect

🖼 To change the image:  
- Replace `assets/flashbang.jpg` with your own full-screen image

---

## 🧪 How to Run

### 🚀 Normal Mode (X11 or Wayland)
```bash
python3 flashbang.py
```

### ⚡ Manual Test Mode
```bash
python3 flashbang.py --trigger
```

### 🩻 Run in Background (Safe from terminal close)
```bash
nohup python3 flashbang.py &
```

Or disown:
```bash
python3 flashbang.py & disown
```

---

## 🪟 Global F10 Hotkey (X11 only)

- Works out of the box on X11 (needs `sudo`)
```bash
sudo python3 flashbang.py
```

---

## 🌀 Wayland Support (Hyprland)

- Add this to `~/.config/hypr/hyprland.conf`:

```ini
bind = ,F10, exec, python /absolute/path/to/flashbang.py --trigger
```

This gives you a working flashbang even without global keyhooks.

---

## 🛠 Run on Startup (systemd user service)

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
ExecStart=/usr/bin/python3 /absolute/path/to/flashbang.py
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

## 🧠 Tips

- Flashbangs occur when you least expect it.
- Use with caution. Or don’t. 😈
- Best paired with memes, or obnoxiously loud SFX.
- Feel free to remaster!

---

## 📜 License

BSD-3 Clause

## quick info
Do what you want. Just don’t sue me when you flashbang your boss.