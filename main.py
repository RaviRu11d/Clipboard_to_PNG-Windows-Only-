import os
import time
from datetime import datetime

from PIL import ImageGrab

from clipboard import copy_file_to_clipboard

SAVE_DIR = "temp"
os.makedirs(SAVE_DIR, exist_ok=True)

print("Watching clipboard...")

processed = False

while True:
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

    time.sleep(0.5)