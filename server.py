import socket
import threading
from datetime import datetime
import os

HOST = '0.0.0.0'  
PORT = 55555      
MAX_CONNECTIONS = 5  
SERVER_PASSWORD = "blkwr" 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(MAX_CONNECTIONS) 

clients_map = {}

def broadcast(message, current_client=None):
    """Sends a packet to all connected clients except the sender."""
    for client in list(clients_map.keys()):
        if client != current_client:
            try:
                client.send(message)
            except:
                remove(client)

def handle_client(client):
    """Listens for data from a specific client and prints it to the console."""
    while True:
        try:
            message = client.recv(4096)
            if message:
                # Server-side logging with timestamp
                timestamp = datetime.now().strftime("%m/%d/%Y; %H:%M:%S")
                try:
                    # Attempt to decode to see if it's a plaintext system leave signal
                    decoded = message.decode('utf-8')
                    if not decoded.startswith("SYSTEM_LEAVE_SIGNAL:"):
                        print(f"[{timestamp}] Incoming Transmission: {decoded}")
                except:
                    # If it's encrypted binary chat data, print the representation
                    print(f"[{timestamp}] Incoming Encrypted Payload: {message}")

                broadcast(message, client)
            else:
                remove(client)
                break
        except:
            remove(client)
            break

def remove(client):
    """Removes a client and safely alerts others of the departure."""
    if client in clients_map:
        nickname = clients_map[client]
        del clients_map[client]
        client.close()
        
        timestamp = datetime.now().strftime("%m/%d/%Y; %H:%M:%S")
        print(f"[{timestamp}] {nickname} disconnected.")
        
        leave_signal = f"SYSTEM_LEAVE_SIGNAL:{nickname}"
        broadcast(leave_signal.encode('utf-8'))

print(f"Secure Server is running. Limit: {MAX_CONNECTIONS} users. Listening on port {PORT}...")
print("Public IP is:")
os.system("curl ifconfig.me")
print()
while True:
    try:
        client_socket, address = server.accept()
        
        if len(clients_map) >= MAX_CONNECTIONS:
            client_socket.close()
            continue

        # --- HANDSHAKE ---
        client_socket.settimeout(4.0)
        client_socket.send("AUTH_REQUEST".encode('utf-8'))
        provided_password = client_socket.recv(1024).decode('utf-8')
        
        if provided_password == SERVER_PASSWORD:
            client_socket.send("NICKNAME_REQUEST".encode('utf-8'))
            provided_nickname = client_socket.recv(1024).decode('utf-8')
            
            clients_map[client_socket] = provided_nickname
            
            # Simplified clean server print without raw IPs/Ports
            timestamp = datetime.now().strftime("%m/%d/%Y; %H:%M:%S")
            print(f"[{timestamp}] {provided_nickname} verified and active.")
            
            online_count = len(clients_map)
            client_socket.send(f"ONLINE_COUNT:{online_count}".encode('utf-8'))
            
            client_socket.settimeout(None) 
            
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
        else:
            client_socket.close()
            
    except Exception as e:
        try:
            client_socket.close()
        except:
            pass