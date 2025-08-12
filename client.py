import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080

def create_socket(protocol) -> socket.socket:
    sock = socket.socket(socket.AF_INET, protocol)
    sock.connect( (HOST, PORT) )
    return sock

def print_key(event):
    key = event.name
    print(key)

    # TODO: translate edge cases

def process_input(sock : socket.socket):
    while True:
        msg = sock.recv(1024).decode()
        print(msg)

def send_screen():
    pass
    # TODO: send screenshots fromto the server


input_sock = create_socket(socket.SOCK_STREAM) # TCP
screen_sock   = create_socket(socket.SOCK_STREAM) # UCP

threading.Thread(target=process_input, args=(input_sock,)).start()