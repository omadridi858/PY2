import os
os.system('Xvfb :1 -screen 0 1600x1200x16  &')  # start it
os.environ['DISPLAY']=':1.0'  # tells X clients where to connect to
from tkinter import *
import customtkinter

root = customtkinter.CTk()
root.geometry("300x400")
def g():
    print('gg')
button1 = customtkinter.CTkButton(master=root, text="Hello World!",command= g)

button1.place(relx=0.5, rely=0.5, anchor=CENTER)
button2 = customtkinter.CTkButton(master=root, text="hi",command= g)

button2.place(relx=0.5, rely=0.7, anchor=CENTER)

root.mainloop()
