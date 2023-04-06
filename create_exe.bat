@echo off
pyinstaller --onefile --icon imgs/icon_stamp_dark.ico stamp_converter.py
copy /Y dist\stamp_converter.exe stamp_converter.exe