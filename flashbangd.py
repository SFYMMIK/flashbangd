import sys
import random
import time
import threading
import configparser
import os

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap, QGuiApplication
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation

import pygame

# Detect session type
is_wayland = os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
is_x11 = not is_wayland

try:
    if is_x11:
        import keyboard
except ImportError:
    print("❌ 'keyboard' module not installed. Run: pip install keyboard")

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
    delay_min = int(config["settings"].get("delay_min", 45))
    delay_max = int(config["settings"].get("delay_max", 600))
    image_path = config["settings"].get("image", "assets/flashbang.jpg")
    sound_path = config["settings"].get("sound", "assets/flashbang.mp3")

    # Initialize sound early for zero-latency
    pygame.mixer.init()
    sound = pygame.mixer.Sound(sound_path)

    app = QApplication(sys.argv)
    flasher = Flashbang(image_path)

    def trigger_flashbang():
        flasher.trigger()
        sound.play()

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

    if is_x11:
        try:
            keyboard.add_hotkey("f10", trigger_flashbang)
            print("✅ Global hotkey F10 registered.")
        except Exception as e:
            print(f"❌ Could not register F10: {e}")
    elif is_wayland:
        print("⚠️ Wayland detected — global hotkeys not supported.")
        print("💡 Use: `--trigger` with a Hyprland keybind.")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
