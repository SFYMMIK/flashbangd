import sys
import random
import time
import threading
import configparser
import os
import platform

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGraphicsOpacityEffect, QSystemTrayIcon, QMenu, QAction
from PyQt6.QtGui import QPixmap, QGuiApplication, QIcon
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation

import pygame

# Detect OS and session type
is_windows = platform.system() == "Windows"
is_wayland = os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
is_x11 = not is_windows and not is_wayland

# Optional hotkey support (Linux/X11 or Windows only)
try:
    import keyboard
    keyboard_available = True
except ImportError:
    print("❌ 'keyboard' module not installed. Run: pip install keyboard")
    keyboard_available = False

class Flashbang:
    def __init__(self, image_path):
        self.subwindows = []
        self.image_path = image_path
        self.setup_windows()

    def setup_windows(self):
        screens = QGuiApplication.screens()
        for screen in screens:
            sub = QWidget()
            sub.setWindowFlags(
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.Tool
            )
            sub.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            sub.setCursor(Qt.CursorShape.BlankCursor)
            sub.setGeometry(screen.geometry())

            label = QLabel(sub)
            label.setPixmap(
                QPixmap(self.image_path).scaled(
                    screen.geometry().width(), screen.geometry().height(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            label.setGeometry(0, 0, screen.geometry().width(), screen.geometry().height())

            effect = QGraphicsOpacityEffect()
            label.setGraphicsEffect(effect)
            effect.setOpacity(1.0)

            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(1500)
            anim.setStartValue(1.0)
            anim.setEndValue(0.0)
            anim.finished.connect(sub.hide)

            sub.label = label
            sub.effect = effect
            sub.anim = anim
            self.subwindows.append(sub)

    def trigger(self):
        for sub in self.subwindows:
            sub.effect.setOpacity(1.0)
            sub.showFullScreen()
            QTimer.singleShot(2000, sub.anim.start)

def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    image_path = os.path.normpath(config["settings"].get("image", "assets/flashbang.jpg"))
    sound_path = os.path.normpath(config["settings"].get("sound", "assets/flashbang.mp3"))

    # Get delay range from config only if available and valid
    try:
        delay_min = int(config["settings"]["delay_min"])
        delay_max = int(config["settings"]["delay_max"])
    except (KeyError, ValueError):
        print("⚠️ Invalid or missing delay_min/delay_max in config.ini")
        delay_min, delay_max = 45, 600  # fallback defaults

    # Initialize sound
    pygame.mixer.init()
    sound = pygame.mixer.Sound(sound_path)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    flasher = Flashbang(image_path)

    def trigger_flashbang():
        flasher.trigger()
        sound.play()

    # System tray icon
    tray = QSystemTrayIcon(QIcon(image_path), parent=app)
    menu = QMenu()
    trigger_action = QAction("Trigger Flashbang")
    trigger_action.triggered.connect(trigger_flashbang)
    quit_action = QAction("Quit")
    quit_action.triggered.connect(app.quit)
    menu.addAction(trigger_action)
    menu.addSeparator()
    menu.addAction(quit_action)
    tray.setContextMenu(menu)
    tray.setToolTip("flashbangd")
    tray.show()

    if "--trigger" in sys.argv:
        trigger_flashbang()
        sys.exit(app.exec())

    def flashbang_loop():
        while True:
            wait_time = random.randint(delay_min, delay_max)
            print("🕶️ Wanna know when the next flashbang is?\n   Find out yourself. :))))")
            time.sleep(wait_time)
            trigger_flashbang()

    threading.Thread(target=flashbang_loop, daemon=True).start()

    if keyboard_available:
        try:
            keyboard.add_hotkey("f10", trigger_flashbang)
            print("✅ Global hotkey F10 registered.")
        except Exception as e:
            print(f"❌ Could not register F10: {e}")
    else:
        print("⚠️ Global hotkey support not available.")
        print("💡 Use: `--trigger` to manually trigger the flashbang.")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
