import socket
import threading
import keyboard
import ctypes
import win32api
from time import sleep
from PIL import Image
import mss
import numpy
import io
import struct
import tkinter

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080

def create_socket(protocol) -> socket.socket:
    sock = socket.socket(socket.AF_INET, protocol)
    sock.connect( (HOST, PORT) )
    return sock

def send_settings():
    ctypes.windll.user32.SetProcessDPIAware()

    sock = create_socket(socket.SOCK_STREAM)
    
    data = struct.pack('!II', win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
    
    sock.send(data)

    sock.close()

def process_input(sock : socket.socket):
    while True:
        buffer = sock.recv(1024).decode()

        while buffer:
            try:
                command, buffer = buffer.split('|', 1)
                print(command)

                action, value = command.split(' ', 1)

                match action:
                    case 'KEY':
                        keyboard.press_and_release(value)

                    case 'MOUSE_MOVE':
                        value = value.split()
                        win32api.SetCursorPos( (int(value[0]), int(value[1])) )
                    
                    case 'MOUSE_CLICK':
                        win32api.mouse_event(int(value), 0, 0, 0, 0)
            except:
                buffer = False
            

# Get byte data from image and break it into chunks
def image_to_chunks(img, chunk_size = 1024):
    # Transform image to binary
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=50)
    image_bytes = buf.getvalue()

    # Create a list of chunks from the byte data using list comprehension
    return [
        image_bytes[i:i + chunk_size] for i in range(0, len(image_bytes), chunk_size)
    ]

def send_screen(sock : socket.socket):
    sct = mss.mss()
    frame_id = 0

    while True:
        # Capture screen
        monitor = sct.monitors[1]
        frame = numpy.array(sct.grab(monitor))
        
        # Convert from RGBA to RGB
        img = Image.fromarray(frame[:, :, :3][:, :, ::-1])
        img = img.resize((1280, 720))
        
        # Break image into chunks
        chunk_arr = image_to_chunks(img)
        total_chunks = len(chunk_arr)

        # Send image in chunks
        for i in range(total_chunks):
            header = struct.pack('!III', frame_id, i, total_chunks)
            sock.sendto(header + chunk_arr[i], server_address)
            sleep(0.001) # Small delay to reduce packet loss

        # Change the next frame's frame_id
        frame_id += 1
        if frame_id > 99:
            frame_id = 0

        sleep(0.01)
    

server_address = (HOST, PORT)
send_settings()
input_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
screen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

input_sock.connect(server_address)

threading.Thread(target=process_input, args=(input_sock,)).start()
threading.Thread(target=send_screen, args=(screen_sock,)).start()

# input_sock.close()
# screen_sock.close()

