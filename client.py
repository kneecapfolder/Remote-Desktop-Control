import socket
import threading
import keyboard
import win32api

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
        command = sock.recv(1024).decode()
        command = command.split()

        match command[0]:
            case 'KEY':
                keyboard.press_and_release(command[1])

            case 'MOUSE_MOVE':
                win32api.SetCursorPos( (int(command[1]), int(command[2])) )
            
            case 'MOUSE_CLICK':
                win32api.mouse_event(int(command[1]), 0, 0, 0, 0)

                    

        print(command)

def send_screen():
    pass
    # TODO: send screenshots fromto the server


input_sock = create_socket(socket.SOCK_STREAM) # TCP
screen_sock   = create_socket(socket.SOCK_STREAM) # UCP

threading.Thread(target=process_input, args=(input_sock,)).start()