from tkinter import *
import os
try:
  from pyscreenshot import grab
  from pynput.keyboard import GlobalHotKeys
  from pynput import mouse
  from pytesseract import pytesseract
  from gtts import gTTS
  from pydub import AudioSegment
  from pydub.playback import play
except:
  import pip
  pip.main(["install", "-r", "requirements.txt"])
  

root = Tk()
shown = False
points = [0, 0]
p = 0
im = 0
tesseract = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

def on_click(x, y, button, pressed):
  global points, p, shown, root, im, tesseract
  if pressed:
    if shown == True and button == mouse.Button.left:
      if p == 1:
        root.attributes('-fullscreen',False)
        root.iconify()
        shown=False
        im = grab(bbox=(points[0], points[1], x, y))
        pytesseract.tesseract_cmd = tesseract
        text = pytesseract.image_to_string(im)
        myobj = gTTS(text=text, lang='en', slow=False)
        myobj.save("text.mp3")
        read = AudioSegment.from_mp3("text.mp3")
        play(read)
        os.remove("text.mp3")
        p = 0
      else:
        points[0] = x
        points[1] = y
        p = 1

def on_press():
  global shown, root
  if shown:
    root.attributes('-fullscreen',False)
    root.iconify()
    shown=False
  else:
    root.attributes('-fullscreen',True)
    root.focus_force()
    root.deiconify()
    shown=True


root.withdraw()
root.attributes('-alpha',0.5)
root.wm_attributes("-toolwindow", True)

listener = mouse.Listener(
    on_click=on_click)
with GlobalHotKeys({'<ctrl>+l': on_press}) as hk:
    listener.start()
    root.mainloop()
    hk.stop()
    hk.join()
    listener.stop()
    listener.join()
