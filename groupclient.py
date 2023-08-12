import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    HOST = HOST_textbox.get().strip()
    PORT = int(PORT_textbox.get().strip())
    username = username_textbox.get().strip()
    password = password_textbox.get().strip()

    if not HOST or not PORT or not username or not password:
        messagebox.showerror("Invalid input", "All fields must be filled")
        return

    client_socket.connect((HOST, PORT))
    credentials = f"{username}:{password}"
    client_socket.send(credentials.encode())
    
    response = client_socket.recv(4096).decode('utf-8')

    if response == '[AUTH_SUCCESS]':
        threading.Thread(target=listen_for_messages_from_server, args=(client_socket,)).start()
        username_textbox.config(state=tk.DISABLED)
        password_textbox.config(state=tk.DISABLED)
        HOST_textbox.config(state=tk.DISABLED)
        PORT_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Authentication Failed", "Invalid username or password")

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

    formatted_message = f'[PM][{username_textbox.get()}] {message}'  # Format the message
    add_message(formatted_message)  # Display the message in the sender's window

    client_socket.send(f"@{recipient} {message}".encode())
    message_textbox.delete(0, tk.END)

def listen_for_messages_from_server(client_socket):
    while True:
        try:
            message = client_socket.recv(4096).decode('utf-8')
            add_message(message)
        except Exception as e:
            print(f'Error while receiving message: {e}')
            break

# ... rest of the code remains unchanged ...


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

password_label = tk.Label(top_frame, text="Password:")
password_label.pack(side=tk.LEFT)

password_textbox = tk.Entry(top_frame, bg="white", fg="black", show="*")
password_textbox.pack(side=tk.LEFT, padx=(0, 10))

HOST_label = tk.Label(top_frame, text="Server IP:")
HOST_label.pack(side=tk.LEFT)

HOST_textbox = tk.Entry(top_frame, bg="white", fg="black")
HOST_textbox.pack(side=tk.LEFT, padx=(0, 10))

PORT_label = tk.Label(top_frame, text="PORT:")
PORT_label.pack(side=tk.LEFT)

PORT_textbox = tk.Entry(top_frame, bg="white", fg="black")
PORT_textbox.pack(side=tk.LEFT, padx=(0, 10))

username_button = tk.Button(top_frame, text="Connect", command=connect, bg="blue", fg="white")
username_button.pack(side=tk.LEFT)

# Create the message box in the middle frame
message_box = scrolledtext.ScrolledText(middle_frame, wrap=tk.WORD, state=tk.DISABLED, bg="purple", fg="white")
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








