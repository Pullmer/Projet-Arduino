# coding: utf-8 

import time
import socket
import Tkinter as tk


TCP_IP = '10.0.0.202'
TCP_PORT = 1111
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

pressedUp = False
pressedDown = False
pressedLeft = False
pressedRight = False

lsKey=['0','0','0','0'] #list of key pressed


#initialisation de la communication wifi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connexion...")

sock.connect((TCP_IP,TCP_PORT))

print("Connected !")

def commandage():
    global lsKey

    a = (lsKey[2]=='1')
    b = (lsKey[3]=='1')
    c = (lsKey[0]=='1')
    d = (lsKey[1]=='1')

    A=(a and not b) or (a and not c and d) or (not b and not c)
    B=(not c and d) or (not a and not b and c and not d) or (a and b and c and not d) or (not a and b and not c) or (not a and b and d) or (a and not b and not c) or (a and not b and d)
    C=(a and not b) or (a and c) or (not b and not d)
    D=(c and not d) or (not a and b and c) or (not a and b and not d) or (a and not b and c) or (a and not b and not d) or (not a and not b and not c and d) or (a and b and not c and d)

    s = "#speedO;"

    if not A:
        s += '-'

    if B:
        s += "70"
    else:
        s += "0"

    s+=';'

    if not C:
        s += '-'

    if D:
        s += "70"
    else:
        s += "0"

    s += ";:"
    
    sock.send(s)
    

def onKeyPress(event):
    global pressedUp
    global pressedDown
    global pressedLeft
    global pressedRight
    global lsKey
    
    if (event.keysym=='Up') and not pressedUp:
        pressedUp = True
        lsKey[0]='1'
        print("".join(lsKey))
        commandage()
    elif (event.keysym=='Down') and not pressedDown:
        pressedDown = True;
        lsKey[1]='1'
        print("".join(lsKey))
        commandage()
    elif (event.keysym=='Left') and not pressedLeft:
        pressedLeft = True;
        lsKey[2]='1'
        print("".join(lsKey))
        commandage()
    elif (event.keysym=='Right') and not pressedRight:
        pressedRight = True;
        lsKey[3]='1'
        print("".join(lsKey))
        commandage()

    
        

def onKeyRelease(event):
    global pressedUp
    global pressedDown
    global pressedLeft
    global pressedRight
    global lsKey
    
    if (event.keysym=='Up'):
        pressedUp = False
        lsKey[0]='0'
        print("".join(lsKey))
        commandage()
    elif (event.keysym=='Down'):
        pressedDown = False;
        lsKey[1]='0'
        print("".join(lsKey))
        commandage()
    elif (event.keysym=='Left'):
        pressedLeft = False;
        lsKey[2]='0'
        print("".join(lsKey))
        commandage()
    elif (event.keysym=='Right'):
        pressedRight = False;
        lsKey[3]='0'
        print("".join(lsKey))
        commandage()




root = tk.Tk()
root.geometry('300x200')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', onKeyPress)
root.bind('<KeyRelease>', onKeyRelease)
root.mainloop()


	

