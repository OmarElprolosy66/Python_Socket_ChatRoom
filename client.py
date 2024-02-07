import socket
import threading

PORT: int           =    5050
FORMAT: str         =   'utf-8'
SERVER: str         =   '127.0.0.1'
ADDRESS: tuple      =   (SERVER, PORT) 
BUFFER_SIZE: int    =   1024

# Get the user's nickname
nickname: str = input('Enter your nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def receive() -> None:
    """
    Receive and display messages from the server.
    """
    while True:
        try:
            message: str = client.recv(BUFFER_SIZE).decode(FORMAT)
            
            if message == "NECK":
                client.send(nickname.encode(FORMAT))
            else:
                print(message)
        except Exception as e:
            print(f"\n{e}\n")
            client.close()
            break

def write() -> None:
    """
    Get user input and send messages to the server.
    """
    while True:
        message: str = f"{nickname}: {input('')}"
        client.send(message.encode(FORMAT))

# Create threads for receiving and writing messages
receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

if __name__ == "__main__":
    # Start the threads
    receive_thread.start()
    write_thread.start()