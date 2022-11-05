import socket
from chat import *

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    listen_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    listen_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    listen_socket.listen()
    chat_socket, address = listen_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:

        if(do_reciever(chat_socket)):
            break

        if(do_sender(chat_socket)):
            break

    chat_socket.close()  # close the connection


if __name__ == '__main__':
    server_program()