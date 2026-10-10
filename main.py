import os
import time
import threading
from datetime import datetime

from PIL import Image, ImageDraw, ImageGrab
import pystray
from pystray import MenuItem as item

from clipboard import copy_file_to_clipboard


SAVE_DIR = "temp"
os.makedirs(SAVE_DIR, exist_ok=True)


class ClipboardWatcher:
    def __init__(self):
        self.running = False
        self.paused = False
        self.thread = None

    def watch_clipboard(self):
        """Background thread function to watch clipboard"""
        processed = False

        while self.running:
            if not self.paused:
                try:
                    data = ImageGrab.grabclipboard()

                    # If clipboard contains an image
                    if hasattr(data, "save"):
                        if not processed:
                            filename = datetime.now().strftime("Screenshot_%Y-%m-%d_%H-%M-%S.png")
                            filepath = os.path.join(SAVE_DIR, filename)

                            data.save(filepath, "PNG")

                            copy_file_to_clipboard(os.path.abspath(filepath))

                            print(f"Saved: {filepath}")

                            processed = True
                    else:
                        processed = False

                except Exception as e:
                    print(f"Error watching clipboard: {e}")

            time.sleep(0.5)

    def start(self):
        """Start the clipboard watcher"""
        if not self.running:
            self.running = True
            self.paused = False
            self.thread = threading.Thread(target=self.watch_clipboard, daemon=True)
            self.thread.start()
            print("Clipboard watcher started")

    def stop(self):
        """Stop the clipboard watcher"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        print("Clipboard watcher stopped")

    def pause(self):
        """Pause the clipboard watcher"""
        self.paused = True
        print("Clipboard watcher paused")

    def resume(self):
        """Resume the clipboard watcher"""
        self.paused = False
        print("Clipboard watcher resumed")


def create_image():
    """Create a simple icon for the system tray"""
    # Create a simple blue square with white "C" for Clipboard
    image = Image.new('RGB', (64, 64), color='blue')
    dc = ImageDraw.Draw(image)
    dc.text((20, 20), "C", fill='white')
    return image


# Global references
watcher = None
tray_icon = None


def on_exit(icon, item):
    """Handle exit action"""
    print("Exit clicked")
    global watcher, tray_icon
    if watcher:
        watcher.stop()
    if tray_icon:
        tray_icon.stop()


def on_toggle(icon, item):
    """Handle pause/resume toggle"""
    global watcher
    print(f"Toggle clicked, current paused state: {watcher.paused if watcher else 'No watcher'}")
    if watcher:
        if watcher.paused:
            watcher.resume()
            print("Watcher resumed")
        else:
            watcher.pause()
            print("Watcher paused")
    # Update the menu immediately
    update_menu()


def update_menu():
    """Update the tray icon menu based on current state"""
    global tray_icon, watcher
    if tray_icon and watcher:
        if watcher.paused:
            tray_icon.menu = pystray.Menu(
                item('Resume', on_toggle),
                item('Exit', on_exit)
            )
        else:
            tray_icon.menu = pystray.Menu(
                item('Pause', on_toggle),
                item('Exit', on_exit)
            )


def setup_tray():
    """Setup system tray icon and menu"""
    global watcher, tray_icon
    watcher = ClipboardWatcher()

    # Start the watcher
    watcher.start()

    # Create icon
    image = create_image()
    tray_icon = pystray.Icon("ClipboardToPNG", image, "Clipboard to PNG Watcher")

    # Set initial menu
    update_menu()

    # Run the icon
    tray_icon.run()


if __name__ == "__main__":
    setup_tray()