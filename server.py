import socket
from tkinter import *
from tkinter import filedialog
import os

def save_file(conn):
    # Receive the file name
    file_name = conn.recv(1024).decode()
    
    # Set the destination folder to save the file
    directory = os.path.join(os.getcwd(), 'Received')
    os.makedirs(directory, exist_ok=True)
    destination = os.path.join(directory, file_name)
    
    # Receive the file data and save it to the destination folder
    with open(destination, 'wb') as file:
        data = conn.recv(1024)
        while data:
            file.write(data)
            data = conn.recv(1024)
    
    print('File successfully received:', file_name)

def start_server():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    # Bind the socket to a specific host and port
    s.bind((ip_address, 8080))
    
    # Listen for incoming connections
    s.listen(1)
    print('Server listening on', s.getsockname()[0])
    
    # Accept a client connection
    conn, addr = s.accept()
    print('Connected to client:', addr[0])
    
    # Save the received file
    save_file(conn)
    
    # Close the connection
    conn.close()

def start_server_button_clicked():
    start_server_button.config(state=DISABLED)
    start_server_button.config(text="Server Running")
    start_server()

# Create the UI
root = Tk()
root.title("Server (Receiver)")
root.configure(bg='#B0E2FF')
icon = PhotoImage(file='../assets/received.png')
root.iconphoto(False, icon)
bg_img = PhotoImage(file='../assets/id.png')
Label(root,image=bg_img,bg='#B0E2FF').place(x=25, y=0)
root.geometry("300x250")
root.resizable(False,False)

start_server_button = Button(root, text="Start Server", command=start_server_button_clicked)
start_server_button.pack(pady=20)
start_server_button.configure(width=16, height=1 , bg='royal blue', fg='white',font=('Arial',10,"bold"))
start_server_button.place(x=80,y=27)

root.mainloop()
