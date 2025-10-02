#listen for incoming connections
#spawn a new thread for each connection
#receive messages from clients and broadcast them to all connected clients

#imports
from ast import arg
from concurrent.futures import thread
import socket
import threading

#server setup
host = '0.0.0.0' #listen on all interfaces
port = 12345 #port to listen on

#creating the connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

#broadcast fuction to send message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

#handle messages from clients
def handle_client(client):
    while True:
        try:
            #receive message from client
            message = client.recv(1024)
            if not message:
                break
            broadcast(message)        
        except:
            #remove and close client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat.' .encode('utf-8'))
            nicknames.remove(nickname)
            break
        
#receive /accept new clients
def receive():
    print("Server is running and listening...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        #request and store username
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))
        
        #start handling thread for client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        
if __name__ == "__main__":
    receive()
    
    