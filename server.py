import socket
import threading
import keyboard
import win32api
import win32con
from time import sleep
from PIL import ImageGrab, Image, ImageTk
import struct
import io
import GUI

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
            root_x, root_y = app.get_root_cordinates()
            sock.sendall(f'MOUSE_MOVE {x - root_x} {y - root_y} '.encode())
            prev_x, prev_y = x, y

        # Left
        if win32api.GetAsyncKeyState(1) & 0x8000:
            if not left:
                left = True
                sock.sendall(f'MOUSE_CLICK {win32con.MOUSEEVENTF_LEFTDOWN} '.encode())
        elif left:
            if not right:
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
def process_screen(server : socket.socket):
    recived_packets = {}
    while True:
        packet, addr = server.recvfrom(2048)
        curr_frame = -1

        # Get header (8 bytes -> 2 integers)
        frame_id, syn, total_packets = struct.unpack('!III', packet[:12]) # Get header
        data = packet[12:] # Get data

        recived_packets[syn] = data

        if curr_frame == -1:
            curr_frame = frame_id
        elif curr_frame != frame_id:
            curr_frame = frame_id
            recived_packets.clear()

        if len(recived_packets) == total_packets:
            curr_frame = -1
            img_data = b''

            # Add all packets in order
            for i in range(total_packets):
                img_data += recived_packets[i]

            recived_packets.clear()

            img = Image.open(io.BytesIO(img_data))
            app.update_screen(ImageTk.PhotoImage(img.resize((1920, 1080), Image.LANCZOS)))
            

input_server  = create_server(socket.SOCK_STREAM) # TCP
screen_server = create_server(socket.SOCK_DGRAM)  # UDP

input_server.listen(5)

threading.Thread(target=send_input, args=(input_server,)).start()
threading.Thread(target=process_screen, args=(screen_server,)).start()

app = GUI.AppInterface()


app.start()
input_server.close()
screen_server.close()