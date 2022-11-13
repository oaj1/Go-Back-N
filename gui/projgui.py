from tkinter import *
import tkinter
import os
import tkinter.messagebox

window = tkinter.Tk()
window.title("COSC635 Project GUI")
window.geometry("300x300")
menu = Menu(window)
# define input 
def sawReceive():
    os.system('python3 sawr.py') # replace with actual code
    
def sawSend(): # pass input variable for packet loss
    os.system('python3 saws.py') # replace with actual code

def gbnReceive():
    os.system('python3 gbnr.py') # replace with actual code
    
def gbnSend(): # pass input variable for packet loss
    os.system('python3 gbns.py') # replace with actual code

def instructions():
    instruction = "Select the Desired Protocol and transmission role.  If sending to yourself on the same computer you need to open a separate send/receive window for each transmission direction!"
    tkinter.messagebox.showinfo(title='Help', message=instruction)


window.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='Protocols', menu=filemenu)
filemenu.add_command(label="Stop and Wait Send", command=sawSend)
filemenu.add_command(label="Stop and Wait Receive", command=sawReceive)
filemenu.add_command(label="Go-back-N Send", command=gbnSend)
filemenu.add_command(label="Go-back-N Receive", command=gbnReceive)

filemenu.add_separator()
filemenu.add_command(label='Exit', command=window.quit)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label='Instructions', command=instructions)


window.mainloop()