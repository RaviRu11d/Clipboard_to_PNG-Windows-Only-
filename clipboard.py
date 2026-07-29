import struct
import time

import win32clipboard
import win32con


def copy_file_to_clipboard(filepath):
    # Windows expects a double-null-terminated UTF-16 string
    files = filepath + "\0"
    data = files.encode("utf-16le") + b"\0\0"

    # DROPFILES structure
    dropfiles = struct.pack("IiiII", 20, 0, 0, 0, 1)

    # Retry until clipboard becomes available
    for _ in range(20):
        try:
            win32clipboard.OpenClipboard()
            break
        except Exception:
            time.sleep(0.05)
    else:
        raise RuntimeError("Could not open clipboard")

    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(
            win32con.CF_HDROP,
            dropfiles + data
        )
    finally:
        win32clipboard.CloseClipboard()