try:
  from tkinter import *
  import pyuac
  import os, sys, shutil
  from subprocess import Popen as call
  from win32com.client import Dispatch
except:
  import pip
  pip.main(["install", "-r", "requirements.txt"])
  from tkinter import *
  import pyuac
  import os, sys, shutil
  from subprocess import Popen as call
  from win32com.client import Dispatch

root = Tk()
root.title("ReadOutLoud setup.py")
text = StringVar()
text.set("Installation in \"C:\Program Files\ReadOutLoud\"")
lbl = Label(root, textvariable=text)
lbl.pack(side='top')

div = Frame(root)
div.pack(side='bottom')

def auto_startup():
  global text, next
  path = "C:/Program Files/ReadOutLoud/"
  user = os.getlogin()
  path2 = f"C:/Users/{user}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/"
  path2 = os.path.join(path2, "ReadOutLoud.lnk")
  target = (f"{sys.executable}" if sys.executable.endswith("pythonw.exe") else f"{sys.executable.replace('python.exe', 'pythonw.exe')}")
  arguments = f"\"{path}ReadOutLoud.pyw\""
  wDir = f"{path}"
  icon = (f"{sys.executable}" if sys.executable.endswith("pythonw.exe") else f"{sys.executable.replace('python.exe', 'pythonw.exe')}")
  shell = Dispatch('WScript.Shell')
  shortcut = shell.CreateShortCut(path2)
  shortcut.Targetpath = target
  shortcut.Arguments = arguments
  shortcut.WorkingDirectory = wDir
  shortcut.IconLocation = icon
  shortcut.save()
  text.set("done, click next to close and run")
  next.configure(command = lambda: call("pytonw C:/Program Files/ReadOutLoud/ReadOutLoud.pyw"))

def setup():
  global text, next
  path="C:/Program Files"
  os.mkdir(f"{path}/ReadOutLoud")
  this_path = __file__[:__file__.rfind("\\")]
  for file in os.listdir(this_path):
    if not os.path.isdir(file) and not "README" in file and not "tesseract" in file:
      shutil.copy(f"{this_path}\{file}", f"{path}/ReadOutLoud")
  call(f"{this_path}/tesseract-ocr-setup-3.02.02.exe")
  text.set("done, click next if you want to set up the auto startup")
  next.configure(command = auto_startup)
  
  

next = Button(root, text = "Next", command= setup)
cancel = Button(root, text = "Cancel", command = exit)
cancel.pack(side='right')
next.pack(side='right')

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:        
        root.mainloop()
