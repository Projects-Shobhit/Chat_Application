import socket
import threading

HOST = '127.0.0.1'
PORT = 1234

clients = []
usernames = {}

# Creating a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def broadcast(message, sender=None):
    for client in clients:
        if sender is None or client != sender:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(4096).decode('utf-8')
            if message:
                if message.startswith('@'):
                    recipient, message = message[1:].split(' ', 1)
                    send_personal_message(client, recipient, message)
                else:
                    broadcast(message.encode('utf-8'), client)
            else:
                remove_client(client)
                break
        except:
            remove_client(client)
            break

def remove_client(client):
    if client in clients:
        clients.remove(client)
        username = usernames[client]
        del usernames[client]
        broadcast(f'[SERVER] {username} has left the chat'.encode('utf-8'))

def send_personal_message(sender, recipient, message):
    if recipient in usernames.values():
        for client, username in usernames.items():
            if username == recipient:
                client.send(f'[PM][{usernames[sender]}] {message}'.encode('utf-8'))
                sender.send(f'[PM][{recipient}] {message}'.encode('utf-8'))
                break
    else:
        sender.send(f'[SERVER] User {recipient} does not exist or is offline'.encode('utf-8'))

def listen_for_connections():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('[USERNAME]'.encode('utf-8'))
        username = client.recv(4096).decode('utf-8')
        usernames[client] = username
        clients.append(client)

        print(f"Username: {username}")
        broadcast(f"[SERVER] {username} has joined the chat".encode('utf-8'))
        client.send('[SERVER] You are connected!'.encode('utf-8'))

        threading.Thread(target=handle_client, args=(client,)).start()

print("Server started...")
listen_for_connections()
