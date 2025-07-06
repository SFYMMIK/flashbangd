import wx
import wx.adv
import pygame
import time
import threading
import random
import sys
import os
import platform
import configparser

try:
    import keyboard
    keyboard_available = True
except ImportError:
    print("❌ 'keyboard' module not installed. Run: pip install keyboard")
    keyboard_available = False

is_windows = platform.system() == "Windows"

class FlashbangWindow(wx.Frame):
    def __init__(self, image_path, duration=2000):
        super().__init__(None, style=wx.STAY_ON_TOP | wx.NO_BORDER | wx.FRAME_NO_TASKBAR)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.panel = wx.Panel(self)
        self.bitmap = wx.Bitmap(image_path, wx.BITMAP_TYPE_ANY)
        self.Bind(wx.EVT_PAINT, self.on_paint)

        self.SetSize(wx.GetDisplaySize())
        self.Centre()
        self.ShowFullScreen(True)

        wx.CallLater(duration, self.close)

    def on_paint(self, evt):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        bmp = self.bitmap.ConvertToImage().Scale(*self.GetSize()).ConvertToBitmap()
        dc.DrawBitmap(bmp, 0, 0, True)

    def close(self):
        self.Hide()
        self.Destroy()

class QuitGameDialog(wx.Dialog):
    def __init__(self, parent, on_exit_callback):
        super().__init__(parent, title="Wait what?", size=(300, 150))
        self.on_exit_callback = on_exit_callback
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Exit? That’s not so easy."), 0, wx.ALL | wx.CENTER, 10)

        btns = wx.BoxSizer(wx.HORIZONTAL)
        btn_okay = wx.Button(self, label="Okay")
        btn_what = wx.Button(self, label="What?")
        btns.Add(btn_okay, 0, wx.ALL, 5)
        btns.Add(btn_what, 0, wx.ALL, 5)

        sizer.Add(btns, 0, wx.CENTER)
        self.SetSizer(sizer)

        btn_okay.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())
        btn_what.Bind(wx.EVT_BUTTON, self.show_game)

    def show_game(self, evt):
        self.Destroy()
        GameWindow(None, self.on_exit_callback).Show()

class GameWindow(wx.Frame):
    def __init__(self, parent, on_exit_callback):
        super().__init__(parent, title="Survive", size=(320, 360), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.on_exit_callback = on_exit_callback
        self.target = random.randint(0, 8)
        self.buttons = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="idk survive i guess"), 0, wx.ALL | wx.CENTER, 10)

        grid = wx.GridSizer(3, 3, 5, 5)
        for i in range(9):
            btn = wx.Button(self, label="?", size=(80, 60))
            btn.Bind(wx.EVT_BUTTON, self.handle_click)
            btn.index = i
            self.buttons.append(btn)
            grid.Add(btn, 0, wx.CENTER)
        sizer.Add(grid, 0, wx.ALL | wx.CENTER, 10)
        self.SetSizer(sizer)
        self.Centre()

    def handle_click(self, evt):
        btn = evt.GetEventObject()
        idx = btn.index

        if idx == self.target:
            btn.SetLabel("X")
            dlg = wx.MessageDialog(self, "you are lucky, i will not haunt you unless you fire me up again", "Exit unlocked", wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Destroy()
                self.Destroy()
                self.on_exit_callback()
        else:
            btn.SetLabel("x")
            for b in self.buttons:
                b.Disable()
            self.show_lost_dialog()

    def show_lost_dialog(self):
        dialog = wx.Dialog(self, title="Failure", size=(260, 140))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(dialog, label="okay you lost"), 0, wx.ALL | wx.CENTER, 10)

        btns = wx.BoxSizer(wx.HORIZONTAL)
        retry = wx.Button(dialog, label="Retry")
        okay = wx.Button(dialog, label="Okay")
        btns.Add(retry, 0, wx.ALL, 5)
        btns.Add(okay, 0, wx.ALL, 5)

        sizer.Add(btns, 0, wx.CENTER)
        dialog.SetSizer(sizer)

        retry.Bind(wx.EVT_BUTTON, lambda e: [dialog.Destroy(), self.retry()])
        okay.Bind(wx.EVT_BUTTON, lambda e: [dialog.Destroy(), self.Destroy()])

        dialog.Centre()
        dialog.ShowModal()

    def retry(self):
        self.Destroy()
        GameWindow(None, self.on_exit_callback).Show()

class FlashbangApp(wx.App):
    def OnInit(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        self.image_path = os.path.normpath(self.config["settings"].get("image", "assets/flashbang.jpg"))
        self.sound_path = os.path.normpath(self.config["settings"].get("sound", "assets/flashbang.mp3"))

        try:
            self.delay_min = int(self.config["settings"]["delay_min"])
            self.delay_max = int(self.config["settings"]["delay_max"])
        except:
            self.delay_min, self.delay_max = 45, 600

        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(self.sound_path)

        self.tray = wx.adv.TaskBarIcon()
        self.tray.SetIcon(wx.Icon(self.image_path), "Flashbangd")

        self.menu = wx.Menu()
        flash_item = self.menu.Append(wx.ID_ANY, "Trigger Flashbang")
        quit_item = self.menu.Append(wx.ID_EXIT, "Quit")

        self.tray.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.on_menu)
        self.Bind(wx.EVT_MENU, self.trigger_flashbang, flash_item)
        self.Bind(wx.EVT_MENU, self.quit_dialog, quit_item)

        if "--trigger" in sys.argv:
            self.trigger_flashbang(None)
            wx.CallLater(3000, self.quit)

        threading.Thread(target=self.loop, daemon=True).start()

        if keyboard_available:
            try:
                keyboard.add_hotkey("f10", self.trigger_flashbang)
            except:
                pass

        return True

    def on_menu(self, evt):
        self.tray.PopupMenu(self.menu)

    def trigger_flashbang(self, evt):
        self.sound.play()
        FlashbangWindow(self.image_path)

    def loop(self):
        while True:
            delay = random.randint(self.delay_min, self.delay_max)
            time.sleep(delay)
            wx.CallAfter(self.trigger_flashbang, None)

    def quit_dialog(self, evt):
        QuitGameDialog(None, self.quit).ShowModal()

    def quit(self):
        self.tray.Destroy()
        self.Exit()

if __name__ == "__main__":
    app = FlashbangApp(False)
    app.MainLoop()
