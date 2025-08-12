import socket
import threading
import keyboard
import win32api
import win32con
from time import sleep

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

# Handle keyboard
def keyboard_click(sock : socket.socket, event):
    sock.sendall(f'KEY {event.name} '.encode())

def send_keyboard_input(sock : socket.socket):
    keyboard.on_press(callback=lambda event: keyboard_click(sock, event))
    keyboard.wait()
    

# Handle mouse
def send_mouse_input(sock : socket.socket):
    prev_x, prev_y = win32api.GetCursorPos()
    left = False
    right = False

    while True:
        x, y = win32api.GetCursorPos()
        
        # Detect mouse movement
        if x != prev_x or y != prev_y:
            sock.sendall(f'MOUSE_MOVE {x} {y} '.encode())
            prev_x, prev_y = x, y

        # Left
        if win32api.GetAsyncKeyState(1) & 0x8000:
            left = True
            sock.sendall(f'MOUSE_CLICK {win32con.MOUSEEVENTF_LEFTDOWN} '.encode())
        elif left:
            left = False
            sock.sendall(f'MOUSE_CLICK {win32con.MOUSEEVENTF_LEFTUP} '.encode())

        # Right
        if win32api.GetAsyncKeyState(2) & 0x8000:
            right = True
            sock.sendall(f'MOUSE_CLICK {win32con.MOUSEEVENTF_LEFTDOWN} '.encode())
        elif right:
            right = False
            sock.sendall(f'MOUSE_CLICK {win32con.MOUSEEVENTF_LEFTUP} '.encode())

        sleep(0.01)


# Handle stream
def process_screen(sock : socket.socket):
    while True:
        pass
        # TODO: get the screenshots and pass them to a GUI

input_server  = create_server(socket.SOCK_STREAM) # TCP
screen_server = create_server(socket.SOCK_DGRAM)  # UDP

input_server.listen(5)

threading.Thread(target=send_input, args=(input_server,)).start()
# threading.Thread(screen_server(screen_server, process_screen)).start()


# prev_x, prev_y = win32api.GetCursorPos()
# while True:
#     x, y = win32api.GetCursorPos()
    
#     # Detect mouse movement
#     if x != prev_x or y != prev_y:
#         # sock.sendall(f'MOUSE_MOVE {x} {y} '.encode())
#         prev_x, prev_y = x, y

#     if win32api.GetAsyncKeyState(1) & 0x8000:
#         print('right key pressed')

#     sleep(0.01)