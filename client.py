import socket
from tkinter import *
from tkinter import filedialog , StringVar
from tkinter import ttk
import os
from tkinterdnd2 import *

def select_file():
    file_path = filedialog.askopenfilename(title="Select File")
    file_entry.delete(0, END)
    file_entry.insert(END, file_path)
    file_status.config(text="File selected: " + file_path)
def send_file():
    # Get the server IP address
    server_ip = server_entry.get()
    
    # Get the selected file path
    file_path = file_entry.get()
    
    # Check if both the server IP address and file path are provided
    if server_ip and file_path:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Connect to the server
            s.connect((server_ip, 8080))
            
            # Send the file name
            file_name = os.path.basename(file_path)
            s.send(file_name.encode())
            
            # Send the file data
            with open(file_path, 'rb') as file:
                data = file.read(1024)
                while data:
                    s.send(data)
                    data = file.read(1024)
            
            print('File successfully sent.')
        
        except ConnectionRefusedError:
            print('Connection refused. Make sure the server is running and the port is open.')
        
        # Close the socket connection
        s.close()

    # for sending file
def send_button_clicked():
    send_button.config(state=DISABLED)
    send_file()
    send_button.config(state=NORMAL)

   # Drag and drop functionality 
def on_file_drop(event):
    file_path = event.data
    file_entry.delete(0, END)
    file_entry.insert(END, file_path)
    file_status.config(text="File selected: " + file_path)

   # Get path of file in label and entry
def get_path(event):
    pathLabel.configure(text=event.data)

# Create the UI
# root = Tk()
root = TkinterDnD.Tk()
root.title("Client (Sender)")
root.configure(bg='#f4fdfe')
icon = PhotoImage(file='../assets/send.png')
root.iconphoto(False, icon)
bg_img = PhotoImage(file='../assets/istockphoto.png')
Label(root,image=bg_img,bg='#f4fdfe').place(x=-2, y=0)
root.geometry("400x250")
root.resizable(False,False)

server_label = Label(root, text="Server IP   :",font=('Arial',9,'bold'),bg='#bfdef2')
server_label.pack()
server_label.place(x=30,y=20)

server_entry = Entry(root, width=25,font=('Arial',12))
server_entry.pack(pady=5)
server_entry.place(x=110,y=20)

file_label = Label(root, text="File Name  :" ,font=('Arial',9,'bold'),bg='#bfdef2')
file_label.pack()
file_label.place(x=30,y=60)

file_entry = Entry(root, width=25,font=('Arial',12))
file_entry.pack(pady=5)
file_entry.place(x=110,y=60)

file_status = Label(root, text="**For selecting a file please click on browse button", font=('Arial', 9, 'italic'), fg='gray',bg='#bfdef2')
file_status.pack()
file_status.place(x=30, y=100)

file_button = Button(root, text="Browse", command=select_file)
file_button.configure(width=16,height=1,bg='royal blue',fg='white',font=('Arial',10,'bold'))
file_button.pack(pady=5)
file_button.place(x=30,y=150)

send_button = Button(root, text="Send", command=send_button_clicked)
send_button.configure(width=16,height=1,bg='royal blue',fg='white',font=('Arial',10,'bold'))
send_button.pack()
send_button.place(x=200,y=150)
nameVar = StringVar()

file_entry.drop_target_register(DND_FILES)
file_entry.dnd_bind('<<Drop>>', on_file_drop)

# Register drop target for pathLabel
pathLabel = Label(root, text="Drag and drop here")
pathLabel.drop_target_register(DND_FILES)
pathLabel.dnd_bind('<<Drop>>', get_path)

root.mainloop()
