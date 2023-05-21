# import all the required  modules
import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk


PORT = 55555
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
 
# Create a new client socket
# and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)
 
 
# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):
 
        # chat win which is currently hidden
        self.win = Tk()
        self.win.withdraw()
 
        # login win
        self.login = Toplevel()

        # set the title
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)
        
        # create Labels
        self.pls = Label(self.login, text="Please login to continue", justify=CENTER, font="Arial 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)
        self.labelName = Label(self.login, text="Name: ", font="Arial 12")
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)
 
        # create an entry box for the messages
        self.entryName = Entry(self.login, font="Arial 14")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryName.focus()
 
        # create the Continue Button
        self.go = Button(self.login, text="CONTINUE", font="Arial 14 bold", command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55)

        self.win.mainloop()
 
    def goAhead(self, name):
        self.layout(name)

        rcv = threading.Thread(target=self.receive)
        rcv.start()
 
    # The main layout of the chat
    def layout(self, name):
        self.name = name

        # to show chat window
        self.win.deiconify()
        self.win.title("Chat")
        self.win.resizable(width=False, height=False)
        self.win.configure(width=470, height=550, bg="#F0E68C")

        self.labelHead = Label(self.win, bg="#F0E68C", fg="#000000", text="Chat", font="Arial 14 bold", pady=5)
        self.labelHead.place(relwidth=1)
        
 
        self.text_area = Text(self.win, width=20, height=2, bg="#00008B", fg="#EAECEE", font="Arial 15", padx=5, pady=5) 
        self.text_area.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_area.config(cursor="arrow")

        self.labelBottom = Label(self.win, bg="#F0E68C", height=80) 
        self.labelBottom.place(relwidth=1, rely=0.775)
 
        self.input_text = Entry(self.labelBottom, font="Arial 13")
        self.input_text.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011) 
        self.input_text.focus()
 
        # create a Send Button
        self.send_Button = Button(self.labelBottom, text="Send", font="Arial 10 bold", width=10, bg="#00008B", fg="#FFFFFF", command=lambda: self.write(self.input_text.get()))
        self.send_Button.place(relx=0.77, rely=0.035, relheight=0.02, relwidth=0.22)
 
        # create a scroll bar
        scrollbar = Scrollbar(self.text_area)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.text_area.yview)

        self.text_area.config(state=DISABLED)
 
    # function to start thread for sending messages
    def write(self, msg):
        self.text_area.config(state=DISABLED)
        self.msg = msg
        self.input_text.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
 
    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
 
                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.name.encode("utf-8"))
                else:
                    # insert messages to text box
                    self.text_area.config(state=NORMAL)
                    self.text_area.insert(END,
                                         message+"\n\n")
 
                    self.text_area.config(state=DISABLED)
                    self.text_area.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occurred!")
                client.close()
                break
 
    # function to send messages
    def sendMessage(self):
        self.text_area.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode("utf-8"))
            break
 
 
# create a GUI class object
g = GUI()