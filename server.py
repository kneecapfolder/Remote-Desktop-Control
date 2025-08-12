import socket
import threading
import keyboard

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080

def create_server(protocol) -> socket.socket:
    server = socket.socket(socket.AF_INET, protocol)
    server.bind( (HOST, PORT) )
    return server

def run_server(server : socket.socket, running_fn: callable):
    sock, _ = server.accept()
    running_fn(sock)

# def keyboard_click(sock : socket.socket, event):
#     sock.sendall(event.name.encode())

def send_input(sock : socket.socket):
    keyboard.on_release(callback=lambda event: sock.sendall(event.name.encode()))
    keyboard.wait()

def process_screen(sock : socket.socket):
    while True:
        pass
        # TODO: get the screenshots and pass them to a GUI

input_server  = create_server(socket.SOCK_STREAM) # TCP
screen_server = create_server(socket.SOCK_DGRAM) # UDP
input_server.listen(5)

threading.Thread(run_server(input_server, send_input)).start()
# threading.Thread(screen_server(input_server, process_screen)).start()

