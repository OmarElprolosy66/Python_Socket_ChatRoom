import socket
import threading

# Server configuration
PORT: int           =    5050
FORMAT: str         =   'utf-8'
SERVER: str         =   '127.0.0.1'
ADDRESS: tuple      =   (SERVER, PORT) 
BUFFER_SIZE: int    =   1024


clients: list = []
nicknames: list = []

server: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDRESS)
server.listen()

def broadcast(msg: bytes, sender: socket) -> None:
    """
    Broadcasts a message to all connected clients except the sender.

    Args:
        msg (bytes): The message to broadcast.
        sender (socket): The socket of the sender.
    """
    for client in clients:
        if client != sender:
            client.send(msg)
            
def handle_client(client) -> None:
    """
    Handles communication with an individual client.

    Args:
        client: The client socket.
    """
    while True:
        try:
            message = client.recv(BUFFER_SIZE)
            broadcast(message, client)
        except Exception as e:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode(FORMAT), client)
            nicknames.remove(nickname)
            break

def receive() -> None:
    """
    Listens for incoming connections and handles each client in a separate thread.
    """
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        # Send a prompt for nickname to the client
        client.send("NICK".encode(FORMAT))
        nickname = client.recv(BUFFER_SIZE).decode(FORMAT)
        clients.append(client)
        nicknames.append(nickname)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode(FORMAT), client)

        # Start a new thread to handle the communication with the client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    print("[STARTING]server is starting...")
    receive()