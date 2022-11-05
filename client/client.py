import socket
import os
import tqdm
from sendfile import sendfile


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    message = ""
    filepath = ""

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    while True:
        is_file = input("will you be sending a file?(y/n): ")
        if is_file.lower().strip() == 'y':
            message = 'fs'
            client_socket.send(message.encode())  # send message
            sendfile(client_socket)
        else:
            message = input("send message: ")  # take input
            client_socket.send(message.encode())  # send message


        if (message.lower().strip() == 'bye'):
            break

        data = client_socket.recv(9172).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal


    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
