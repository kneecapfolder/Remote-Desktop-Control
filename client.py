import socket
import threading
import keyboard
import win32api
from time import sleep
from PIL import ImageGrab
import io
import struct

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080

def create_socket(protocol) -> socket.socket:
    sock = socket.socket(socket.AF_INET, protocol)
    sock.connect( (HOST, PORT) )
    return sock

def process_input(sock : socket.socket):
    while True:
        command = sock.recv(1024).decode()
        command = command.split()

        match command[0]:
            case 'KEY':
                keyboard.press_and_release(command[1])

            case 'MOUSE_MOVE':
                win32api.SetCursorPos( (int(command[1]), int(command[2])) )
            
            case 'MOUSE_CLICK':
                win32api.mouse_event(int(command[1]), 0, 0, 0, 0)

# Get byte data from image and break it into chunks
def image_to_chunks(img, chunk_size = 1024):
    # Transform image to binary
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    image_bytes = buf.getvalue()

    # Create a list of chunks from the byte data using list comprehension
    return [
        image_bytes[i:i + chunk_size] for i in range(0, len(image_bytes), chunk_size)
    ]

def send_screen(sock : socket.socket):
    frame_id = 0
    while True:
        chunk_arr = image_to_chunks(ImageGrab.grab())
        total_chunks = len(chunk_arr)

        for i in range(total_chunks):
            header = struct.pack('!III', frame_id, i, total_chunks)
            sock.sendto(header + chunk_arr[i], server_address)
            sleep(0.001) # Small delay to reduce packet loss
        frame_id += 1

        sleep(0.01)

    

server_address = (HOST, PORT)
input_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
screen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

input_sock.connect(server_address)

threading.Thread(target=process_input, args=(input_sock,)).start()
threading.Thread(target=send_screen, args=(screen_sock,)).start()

# input_sock.close()
# screen_sock.close()

