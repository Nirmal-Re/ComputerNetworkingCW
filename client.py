import socket
import sys

HEADER = 30
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def message(msg):
    message_to_send = msg.encode(FORMAT)
    msg_length = len(message_to_send)
    msg_to_send = str(msg_length).encode(FORMAT)
    msg_to_send += b' ' * (HEADER - len(msg_to_send)) + message_to_send
    client.send(msg_to_send)


def read_replies(temp_client):
    msg_length = temp_client.recv(HEADER).decode(FORMAT)
    length_to_read = int(msg_length)
    actual_message = temp_client.recv(length_to_read).decode(FORMAT)
    return actual_message


authorised = True
while authorised:
    userName = input("Enter a permanent Username:")
    message(userName)
    received_msg = read_replies(client)
    print(f"{received_msg}")

    if received_msg != "Not a user":
        authorised = False
        another_received_msg = read_replies(client)
        print(another_received_msg)

    elif received_msg == "TERMINATING...":
        sys.exit()

    else:
        print("Not a valid username!")
        authorised = True
        # sys.exit()


connected = True
while connected:
    msg = input(f"{userName} >>>   ")
    message(msg)
    received_msg2 = read_replies(client)
    print(received_msg2)
    if received_msg2 == "Order Complete":  #DONE
        sys.exit()
    elif received_msg2 == "TERMINATING...": #END
        sys.exit()
    elif received_msg2 == 'Invalid command-- Try again!': #ERR
        msg = read_replies(client)
        print(f"{msg}")
