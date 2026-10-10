@echo off
REM Use start to launch pythonw in the background and immediately close this batch window
start "" "D:\Install_DIR\miniconda3\pythonw.exe" "%~dp0main.py"
exit