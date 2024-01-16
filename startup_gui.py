import tkinter as tk
import webbrowser
import sys
import importlib
from 実験 import main

first_flag = 0

class agent_frame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.var = tk.IntVar()
        self.var.set(1)
        self.pack()
        self.create_widgets()


    def create_widgets(self):
        self.text = tk.Label(self, text = "Agents")
        self.text.pack(side = 'top')
        self.radio_1 = tk.Radiobutton(self,value= 1,variable = self.var,text = "Agent A")
        self.radio_1.pack(side = 'top')
        self.radio_2 = tk.Radiobutton(self,value= 2,variable = self.var,text = "Agent B")
        self.radio_2.pack(side = 'top')

class seed_frame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.var = tk.IntVar()
        self.var.set(1)
        self.pack()
        self.create_widgets()
        

    def create_widgets(self):
        self.text = tk.Label(self, text = "Game Number")
        self.text.pack(side = 'top')
        self.radio = [None for _ in range(5)] 
        for i in range(1,5):
            self.radio[i] = tk.Radiobutton(self,value  = i,variable = self.var , text = str(i))
            self.radio[i].pack(side = 'top')

class start_frame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(self,text = 'start', command = start_server)
        self.start_button.pack(side = 'top')

def start_server():
    global first_flag
    webbrowser.open_new("file:///C:/Users/KawagoeAtsushi/research/hanabi_web/dev/client.html")
    main()
    

root = tk.Tk()
root.title("Hanabi Starter")
f_1 = agent_frame(master = root)
f_1.pack(padx = 40,pady = 40, side = 'left')
f_2 = seed_frame(master = root)
f_2.pack(padx = 40,pady = 40,side = 'right')
f_3 = start_frame(master = root)
f_3.pack(pady = 10,side = 'bottom')
root.mainloop()
