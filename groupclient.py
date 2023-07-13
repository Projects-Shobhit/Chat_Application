import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    username = username_textbox.get().strip()
    if not username:
        messagebox.showerror("Invalid username", "Username cannot be empty")
        return

    client_socket.send(username.encode())

    threading.Thread(target=listen_for_messages_from_server, args=(client_socket,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get().strip()
    if not message:
        messagebox.showerror("Empty message", "Message cannot be empty")
        return

    client_socket.send(message.encode())
    message_textbox.delete(0, tk.END)

def send_personal_message():
    recipient = recipient_textbox.get().strip()
    message = message_textbox.get().strip()
    if not recipient or not message:
        messagebox.showerror("Invalid input", "Recipient and message cannot be empty")
        return

    client_socket.send(f"@{recipient} {message}".encode())
    message_textbox.delete(0, tk.END)

def listen_for_messages_from_server(client_socket):
    while True:
        try:
            message = client_socket.recv(4096).decode('utf-8')
            if message.startswith('[SERVER]'):
                add_message(message)
            elif message.startswith('[PM]'):
                add_message(message[4:])
            else:
                add_message(message)
        except Exception as e:
            print(f'Error while receiving message: {e}')
            break

# GUI Setup
root = tk.Tk()
root.geometry("800x600")
root.title("Messenger Client")

# Create the frames
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

middle_frame = tk.Frame(root)
middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Create the widgets in the top frame
username_label = tk.Label(top_frame, text="Username:")
username_label.pack(side=tk.LEFT)

username_textbox = tk.Entry(top_frame, bg="white", fg="black")
username_textbox.pack(side=tk.LEFT, padx=(0, 10))

username_button = tk.Button(top_frame, text="Connect", command=connect, bg="blue", fg="white")
username_button.pack(side=tk.LEFT)

# Create the message box in the middle frame
message_box = scrolledtext.ScrolledText(middle_frame, wrap=tk.WORD, state=tk.DISABLED, bg="purple",fg="white")
message_box.pack(fill=tk.BOTH, expand=True)

# Create the send message widgets in the bottom frame
message_textbox = tk.Entry(bottom_frame, bg="white", fg="black")
message_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

send_button = tk.Button(bottom_frame, text="Send Message", command=send_message, bg="green", fg="white")
send_button.pack(side=tk.LEFT)

# Create the personal message widgets in the bottom frame
recipient_textbox = tk.Entry(bottom_frame, bg="white", fg="black")
recipient_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

personal_send_button = tk.Button(bottom_frame, text="Send Personal", command=send_personal_message, bg="orange", fg="white")
personal_send_button.pack(side=tk.LEFT)

root.mainloop()
