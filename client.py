import socket
from chat import *

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    chat_socket = socket.socket()  # instantiate
    chat_socket.connect((host, port))  # connect to the server

    while True:
        if(do_sender(chat_socket)):
            break

        if(do_reciever(chat_socket)):
            break


    chat_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
