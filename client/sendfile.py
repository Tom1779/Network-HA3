import os
import tqdm

SEPARATOR = "<SEPERATOR>"
BUFFER_SIZE = 4096

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
                unit_divisor=1024)
            with open(filepath, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    print(f'Read {len(bytes_read)} from {filepath}')
                    if not bytes_read:
                        # file transmitting is done
                        # client_socket.sendall(bytes_read)
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
