import os, sys
from win32com.client import Dispatch

path = __file__[:__file__.rfind("\\")+1]
user = os.getlogin()
path2 = f"C:/Users/{user}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/"
path2 = os.path.join(path2, "ReadOutLoud.lnk")
target = (f"{sys.executable}" if sys.executable.endswith("pythonw.exe") else f"{sys.executable.replace('python.exe', 'pythonw.exe')}")
arguments = f"\"{path}ReadOutLoud.py\""
wDir = f"{path}"
icon = (f"{sys.executable}" if sys.executable.endswith("pythonw.exe") else f"{sys.executable.replace('python.exe', 'pythonw.exe')}")
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path2)
shortcut.Targetpath = target
shortcut.Arguments = arguments
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = icon
shortcut.save()
print("done")
input("Press enter to exit program.")
