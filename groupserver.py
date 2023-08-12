import socket
import threading

HOST = HOST = socket.gethostbyname(socket.gethostname())
PORT = 1234

clients = {}
PASSWORD = "password"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def broadcast(message, sender=None):
    for client, _ in clients.items():
        if sender is None or client != sender:
            client.send(message)

def handle_client(client, username):
    broadcast(f'[SERVER] {username} has joined the chat\n'.encode('utf-8'))

    while True:
        try:
            message = client.recv(4096).decode('utf-8')
            if not message:
                remove_client(client)
                break

            if message.startswith('@'):
                recipient, message = message[1:].split(' ', 1)
                send_personal_message(client, username, recipient, message)
            else:
                broadcast(f'[{username}] {message}'.encode('utf-8'))
        except:
            remove_client(client)
            break

def remove_client(client):
    if client in clients:
        username = clients[client]
        del clients[client]
        broadcast(f'[SERVER] {username} has left the chat\n'.encode('utf-8'))

def send_personal_message(sender, sender_username, recipient, message):
    for client, username in clients.items():
        if username == recipient:
            client.send(f'[PM][{sender_username}] {message}\n'.encode('utf-8'))
            break

def authenticate(client, received_password):
    return received_password == PASSWORD

def listen_for_connections():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        received_credentials = client.recv(4096).decode('utf-8')
        username, received_password = received_credentials.split(':')

        if authenticate(client, received_password):
            clients[client] = username
            client.send('[AUTH_SUCCESS]'.encode('utf-8'))
            print(f"Authenticated: {username}")
            threading.Thread(target=handle_client, args=(client, username)).start()
        else:
            print(f"Authentication failed for {address}")
            client.send('[AUTH_FAILED]'.encode('utf-8'))
            client.close()

print("Server started...")
listen_for_connections()