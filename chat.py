import os
import tqdm

SEPARATOR = "<SEPERATOR>"
BUFFER_SIZE = 4096
UNIT_DIVISOR = 1024


def sendfile(client_socket):
    while True:
        filepath = input("file path: ")
        if os.path.isfile(filepath):
            filesize = os.path.getsize(filepath)
            client_socket.send(f"{filepath}{SEPARATOR}{filesize}".encode())
            progress = tqdm.tqdm(
                range(filesize),
                f"Sending {filepath}",
                unit="B",
                unit_scale=True,
                unit_divisor=UNIT_DIVISOR)
            with open(filepath, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in
                    # busy networks
                    client_socket.sendall(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))
                f.close()
            break
        else:
            print("file does not exist please try again")

def recieve_file(socket):
    print("recieveing file:")
    received = socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    filename = os.path.join("downloads",filename)
    print(filename)
    # convert to integer
    filesize = int(filesize)
    progress = tqdm.tqdm(
        range(filesize), 
        f"Receiving {filename}", 
        unit="B", 
        unit_scale=True, 
        unit_divisor=UNIT_DIVISOR)
    with open(filename, "wb") as f:
        remaining = filesize
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = socket.recv(BUFFER_SIZE)
            f.write(bytes_read)
            progress.update(len(bytes_read))
            remaining -= len(bytes_read)
            if remaining == 0:   
                break
        f.close()
        print("\nfile downloaded succesfully")


def do_sender(socket):
    is_file = input("will you be sending a file?(y/n): ")
    if is_file.lower().strip() == 'y':
        message = 'fs'
        socket.send(message.encode())  # send message
        sendfile(socket)
    else:
        message = input("send message: ")  # take input
        socket.send(message.encode())  # send message

    if (message.lower().strip() == 'bye'):
        return 1
    
    return 0

def do_reciever(socket):
    # receive data stream.
    data = socket.recv(BUFFER_SIZE).decode()
    if not data:
        return 1
    if data.lower().strip() == 'fs':
       recieve_file(socket)
    else:    
        print("from connected user: " + str(data))
        if data.lower().strip() == "bye":
            return 1
    return 0