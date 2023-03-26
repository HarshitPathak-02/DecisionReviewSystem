from functools import partial
import tkinter
import cv2
import PIL.Image, PIL.ImageTk 
import threading
import imutils
import time

stream = cv2.VideoCapture('''clip.mp4''')

def play(speed):
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)#video ko set kiya gaya hai.
    stream.set(cv2.CAP_PROP_POS_FRAMES,frame1+speed)#isse video ki speed ko set kiya gaya hai.
    grabbed,frame = stream.read()#isse video ko read kiya gaya hai.
    if not grabbed :
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)#isse video ko resolution ke anuroop lagaya gaya hai.
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame,anchor= tkinter.NW)#isse video ko position di gai hai.
    canvas.create_text(200, 25, fill='''white''', font='''Times 27 bold''', text='''Decision Pending''')#Video ke upar text lane ke liye haai.
    

def pending(decision):
    # 1.Display decision pending image.
    frame = cv2.cvtColor(cv2.imread('''decision pending.jpg'''), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT) #used for resizing our exisiting image into the size of programes image. 
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    # 2.Wait for one second.
    time.sleep(1)
    # 3.Display Out/not out.
    if decision == '''out''':
        decisionImg = '''out.jpg'''
    else:
        decisionImg = '''not out.jpg'''
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

def out():
    thread = threading.Thread(target=pending, args=('''out''',))
    thread.daemon = 1
    thread.start()
    print('''Player is out''')

def not_out():
    thread = threading.Thread(target=pending, args=('''not out''',))
    thread.daemon = 1
    thread.start()
    print('''Player is not out''')

#width and height of the main screen
SET_WIDTH = 650
SET_HEIGHT = 368

#tkinter gui starts here 
window = tkinter.Tk()
window.title('''Decision Review System''')
cv_img = cv2.cvtColor(cv2.imread('''drs.jpg'''), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

#buttons to control playback
btn = tkinter.Button(window, text='''<< Previous (fast)''', width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text='''<< Previous (slow)''', width=50,command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text='''>> Next (slow)''', width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text='''>> Next (fast)''', width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text=''' Give Out''', width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text=''' Give Not Out''', width=50, command=not_out)
btn.pack()
window.mainloop()