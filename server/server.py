import socket
import os
import tqdm

BUFFER_SIZE = 4096
SEPARATOR = "<SEPERATOR>"

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen()
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(4096).decode()
        if not data:
            # if data is not received break
            break
        if data.lower().strip() == 'fs':
            print("recieveing file:")
            received = conn.recv(BUFFER_SIZE).decode()
            filename, filesize = received.split(SEPARATOR)
            # remove absolute path if there is
            filename = os.path.basename(filename)
            print(filename)
            # convert to integer
            filesize = int(filesize)
            progress = tqdm.tqdm(
                range(filesize), 
                f"Receiving {filename}", 
                unit="B", 
                unit_scale=True, 
                unit_divisor=1024)
            with open(filename, "wb") as f:
                remaining = filesize
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = conn.recv(BUFFER_SIZE)
                    f.write(bytes_read)
                    print(f'Read {len(bytes_read)} from {filename}')
                    progress.update(len(bytes_read))
                    remaining -= len(bytes_read)
                    if remaining == 0:   
                        break
                    # write to the file the bytes we just received
                    # update the progress bar
                f.close()
                print("\nfile downloaded succesfully")
        else:    
            print("from connected user: " + str(data))
            if data.lower().strip() == "bye":
                break
        
        is_file = input("will you be sending a file?(y/n): ")
        if is_file.lower().strip() == 'y':
            while True:
                filepath = input("file path: ")
                if os.path.isfile(filepath):
                    file = open(filepath, "r")
                    message = file.read()
                    conn.send(message.encode())  # send message
                    break
                else:
                    print("file does not exist please try again")
        else:
            message = input("send message: ")  # take input
            conn.send(message.encode())  # send message

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()