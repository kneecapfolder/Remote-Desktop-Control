import socket
import threading
import keyboard
import mouse

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080

def create_server(protocol) -> socket.socket:
    server = socket.socket(socket.AF_INET, protocol)
    server.bind( (HOST, PORT) )
    return server

def send_input(server : socket.socket):
    sock, _ = server.accept()
    threading.Thread(target=send_keyboard_input, args=(sock,)).start()
    threading.Thread(target=send_mouse_input, args=(sock,)).start()

# def run_server(server : socket.socket, running_fn: callable):
#     sock, _ = server.accept()
#     running_fn(sock)

def keyboard_click(sock : socket.socket, event):
    sock.sendall(f'KEY {event.name}'.encode())

def send_keyboard_input(sock : socket.socket):
    keyboard.on_press(callback=lambda event: keyboard_click(sock, event))
    keyboard.wait()
    
def on_mouse_event(sock : socket.socket, event):
    if isinstance(event, mouse.MoveEvent):
        sock.sendall(f'MOUSE_MOVE {event.x} {event.y} '.encode())
    elif isinstance(event, mouse.ButtonEvent):
        sock.sendall(f'MOUSE_MOVE {event.button} {event.event_type}'.encode())

def send_mouse_input(sock : socket.socket):
    mouse.hook(lambda event: on_mouse_event(sock, event))

def process_screen(sock : socket.socket):
    while True:
        pass
        # TODO: get the screenshots and pass them to a GUI

input_server  = create_server(socket.SOCK_STREAM) # TCP
screen_server = create_server(socket.SOCK_DGRAM)  # UDP

input_server.listen(5)

threading.Thread(target=send_input, args=(input_server,)).start()
# threading.Thread(screen_server(input_server, process_screen)).start()

