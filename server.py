import socket
import threading
import sys
from threading import Event

# When I stopped I was structuring messages

users = ['Nirmal', 'Amaar', 'Robyn', 'Patrick']
menus = {'STARTER': ['Garlic Bread', 'Onion Rings', 'Chicken Wings', 'Bacon-Wraped Prawns'],
         'MAIN':['Spaghetti', 'Chicken Tikka Masala', 'Beef Burgers', 'Chicken Madras'],
         'SIDE':['Rice', 'Fries', 'Nan', 'Mac and Cheese']}
order_map = {}
HEADER = 30

# what this header says is the first message to the server every single time from the client
# is going to be header of length 64 that tells us the length of the message that is going to arrive next
# example: if the client is about to send a message that is 5 byte, before sending this message, the client well send
# a message of 64 byte that contains only a number(size) of the message which is 5 in our case to the server so
# server is ready to receive that message.
# the above part is obviously be coded in the client side.


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = "192.168.75.1" # this is the ip address of my machine not the router.
# but the problem with second SERVER is, because it is being hardcoded the code would not work on a different machine
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# af_inet describes what kind of address we are looking for
# SOCK_STREAM describes what method we are using to accept the data from the given address type


server.bind(ADDRESS)


def message(connection, msg):
    send_message = msg.encode(FORMAT)
    msg_length = len(send_message)
    send_msg = str(msg_length).encode(FORMAT)
    send_msg += b' ' * (HEADER - len(send_msg)) + send_message
    connection.send(send_msg)


def read_replies(connection):
    msg_length = connection.recv(HEADER).decode(FORMAT)
    if msg_length:
        length_to_read = int(msg_length)
        actual_message = connection.recv(length_to_read).decode(FORMAT)
        return actual_message



def AUTH(user_name):
    if user_name in users:
        return True


def NEW(connection):
    msg = "You are now able to access the menu or ORDR: "
    message(connection, msg)


def menu():
    p = ''
    counter = 1
    for key in menus:
        p += key + "\n"
        for x in menus[key]:
            temp = str(counter)
            p += "\t" + temp + " : " + x + "\n"
            counter += 1
    return p


def ORDR(user_name, order_list):
    if user_name not in order_map.keys():
        order_map[user_name] = order_list
    elif user_name in order_map.keys():
        for x in order_list:
            order_map[user_name].append(x)


def OLD(user_name):
    pass


def PKUP(user_name):
    p = ''
    counter = 0
    for x in order_map[user_name]:
        temp = str(counter)
        p += temp + " : " + x + "\n"
        counter += 1
    return p


def handle_client(connection, address):
    print(f"CONNECTED TO {address}.")
    connected = True
    counter = 0
    while connected:
        # at this point it is necessary for us to understand how big of the message are we going to accept.
        msg = read_replies(connection)
        print(f"{msg}")

        if msg:
            user = False
            if AUTH(msg):
                user = True
                to_send = "Authorised"
                message(connection, to_send)

            elif msg.upper() == "END":
                to_send = "TERMINATING..."
                message(connection, to_send)
                connected = False
            elif counter == 4:
                connected = False
            else:
                print(f"{msg} isn't one of the user")
                print(f"{counter}")
                to_send = "Not a user"
                message(connection, to_send)
                counter += 1
                connected = True

            while user:
                customer = msg
                print(f"{customer} is now has access to NEW, OLD, and END")
                to_send = "NEW for new customer, OLD to pick up, and END to terminate"
                message(connection, to_send)
                print(f"Waiting for request from the {customer}")

                msg1 = read_replies(connection)
                print(f"{msg1}")

                command1 = False
                if msg1.upper() == "NEW" or msg1.upper() == "OLD":
                    command1 = True
                elif msg1.upper() == "END":
                    to_send = "TERMINATING..."
                    message(connection, to_send)
                    connected = False
                    user = False
                else:
                    to_send = "Invalid command-- Try again!"
                    message(connection, to_send)

                while command1:
                    if msg1.upper() == "NEW":
                        NEW(connection)
                        msg = read_replies(connection).upper()

                        command2 = False
                        if msg == "MENU" or msg == "ORDR":
                            command2 = True
                        elif msg == "END":
                            to_send = "TERMINATING..."
                            message(connection, to_send)
                            connected = False
                            user = False
                            command1 = False
                        else:
                            to_send = "Invalid command-- Try again!"
                            message(connection, to_send)

                        while command2:
                            if msg.upper() == "MENU":
                                print(f"{customer} has envoked menu function \n")
                                ret_message = menu()
                                ret_message += "[If you would like to order type ORDR]"
                                message(connection, ret_message)
                                order = True
                                while order:
                                    msg = read_replies(connection).upper()
                                    if msg == "ORDR":
                                        order = False
                                    elif msg == "END":
                                        to_send = "TERMINATING..."
                                        message(connection, to_send)
                                        connected = False
                                        user = False
                                        command1 = False
                                        order = False
                                    else:
                                        to_send = "Invalid command-- Try again!"
                                        message(connection, to_send)
                                        to_send2 = "Only command you can use is ORDR"
                                        message(connection, to_send2)

                            if msg.upper() == "ORDR":
                                print(f"{customer} has envoked ORDR function")
                                incorrect_starter = True
                                while incorrect_starter:
                                    to_send = "Enter your STARTER from the menu or none, please"
                                    message(connection, to_send)
                                    starter = read_replies(connection)
                                    print(starter)
                                    if starter == "none" or starter == "NONE":
                                        incorrect_starter = False
                                    elif starter not in menus['STARTER']:
                                        incorrect_starter = True
                                    elif starter in menus['STARTER']:
                                        incorrect_starter = False

                                incorrect_main = True
                                while incorrect_main:
                                    to_send = "Enter your MAIN from the menu or none, please"
                                    message(connection, to_send)
                                    main = read_replies(connection)
                                    print(main)
                                    if main == "none" or main == "NONE":
                                        incorrect_main = False
                                    elif main not in menus['MAIN']:
                                        incorrect_main = True
                                    elif main in menus['MAIN']:
                                        incorrect_main = False

                                incorrect_side = True
                                while incorrect_side:
                                    to_send = "Enter your SIDE from the menu or none, please"
                                    message(connection, to_send)
                                    side = read_replies(connection)
                                    if side == "none" or side == "NONE":
                                        incorrect_side = False
                                    elif side not in menus['SIDE']:
                                        incorrect_side = True
                                    elif side in menus['SIDE']:
                                        incorrect_side = False

                                order_list = [starter, main, side]
                                ORDR(customer, order_list)

                                to_send = "Order Complete"
                                message(connection, to_send)
                                connected = False
                                command2 = False
                                print(f"[CLOSED] CONNECTION WITH {customer} CLOSED")
                                sys.exit()

                    elif msg1.upper() == "OLD":
                        if customer in order_map.keys():
                            to_send = f"{customer} can pick up the order using PKUP command."
                            message(connection, to_send)

                            pick_up = True
                            while pick_up:
                                msg = read_replies(connection)
                                if msg.upper() == "PKUP":
                                    ready_order = PKUP(customer) + "\n Thank you for ordering!"
                                    message(connection, ready_order)
                                    pick_up = False
                                    sys.exit()
                                elif msg == "END" or msg == "end":
                                    connection.send("TERMINATING...".encode(FORMAT))
                                    connected = False
                                else:
                                    to_send = "You can only use PKUP command"
                                    message(connection, to_send)

                        else:
                            to_send = "You haven't ordered"
                            message(connection, to_send)


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"NUMBER OF ACTIVE THREADS: {threading.active_count()-1}")


print("[STARTING] server is starting...")
start()

