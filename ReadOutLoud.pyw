from tkinter import *
import os

from audio import *
try:
  from PIL import ImageStat
  from pyscreenshot import grab
  from pynput.keyboard import GlobalHotKeys
  from pynput import mouse
  from pytesseract import pytesseract
  from gtts import gTTS
except:
  import pip
  pip.main(["install", "-r", "requirements.txt"])
  from PIL import ImageStat
  from pyscreenshot import grab
  from pynput.keyboard import GlobalHotKeys
  from pynput import mouse
  from pytesseract import pytesseract
  from gtts import gTTS
  

root = Tk()
shown = False
points = [0, 0]
p = 0
im = 0
audio = Audio()
path = __file__[:__file__.rfind("\\")+1]
tesseract = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
lang = 'en'



def on_click(x, y, button, pressed):
  global points, p, shown, root, im, tesseract, lang
  if pressed:
    if shown == True and button == mouse.Button.left:
      if p == 1:
        root.attributes('-fullscreen',False)
        root.iconify()
        shown=False
        if x < points[0]:
          points[0] ^= x
          x ^= points[0]
          points[0] ^= x
        if y < points[1]:
          points[1] ^= y
          y ^= points[1]
          points[1] ^= y
        im = grab(bbox=(points[0], points[1], x, y))
        thresh = 127
        fn = lambda x : 255 if x > thresh else 0
        im = im.convert('L').point(fn, mode='1')
        s = ImageStat.Stat(im).median
        if s == [0]:
          fn = lambda x : 0 if x > thresh else 255
          im = im.convert('L').point(fn, mode='1')
        pytesseract.tesseract_cmd = tesseract
        text = pytesseract.image_to_string(im)
        myobj = gTTS(text=text, lang=lang, slow=False)
        myobj.save("text.mp3")
        audio.openfile(f"{path}text.mp3")
        audio.play()
        os.remove("text.mp3")
        p = 0
      else:
        if p == -1:
          p = 0
        else:
          points[0] = x
          points[1] = y
          p = 1

def on_press():
  global shown, root
  if shown:
    root.attributes('-fullscreen',False)
    root.attributes('-topmost', False)
    root.iconify()
    root.update()
    shown=False
  else:
    root.attributes('-topmost', True)
    root.attributes('-fullscreen',True)
    root.deiconify()
    root.focus_force()
    root.update()
    shown=True


root.withdraw()
root.attributes('-alpha',0.5)
root.wm_attributes("-toolwindow", True)
var = Variable(value=['en', 'fr'])
listbox = Listbox(
    root,
    listvariable=var,
    height=len(var.get()),
    selectmode=SINGLE
)

listbox.pack()

def items_selected(event):
  global p, lang
  p = 0
  selected_indices = listbox.curselection()
  selected_langs = listbox.get(selected_indices[0])
  lang = selected_langs


listbox.bind('<<ListboxSelect>>', items_selected)

listener = mouse.Listener(
    on_click=on_click)
with GlobalHotKeys({'<ctrl>+l': on_press}) as hk:
    listener.start()
    root.mainloop()
    hk.stop()
    hk.join()
    listener.stop()
    listener.join()
