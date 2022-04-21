import pickle
import socket
import os

print("======== Client ========\n")

CLOSE_CONNECTION = '0'
STORE_FILE = '1'
REQUEST_FILE_LIST = '2'
REQUEST_FILE = '3'

HOST = "localhost"
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("[ Connecting to server ]\n")
client.connect((HOST, PORT))

print("[ Connected ]\n")

while 1:
    print("0 - close connection")
    print("1 - upload file")
    print("2 - request list of available files")
    print("3 - request file\n")

    op = str(input("Choose an option: "))
    print()

    if op == CLOSE_CONNECTION:
        client.send("0".encode())
        break
    elif op == STORE_FILE:
        file_name = str(input("Type the file name: "))
        try:
            with open(file_name, 'rb') as file:
                client.send("1".encode())
                client.send(file_name.encode())

                print(f"\n[ Sending file {file_name} ]\n")
                client.send(str(os.path.getsize(file_name)).encode())

                while True:
                    bytes_read = file.read()
                    if not bytes_read:
                        break
                    client.sendall(bytes_read)
                print(client.recv(1024).decode())
        except FileNotFoundError:
            print(f"\n[ File {file_name} not found ] \n")

    elif op == REQUEST_FILE_LIST:
        list = client.send("2".encode())
        available_files = pickle.loads(client.recv(2048))
        if len(available_files) != 0:
            print("[ Available files ]\n")
            for file in available_files:
                print(f"-> {file}")
            print()
        else:
            print("[ No files available ]\n")

        client.sendall(
            f"[ List of files received successfully! ]\n".encode())
    elif op == REQUEST_FILE:
        file_name = str(input("Type the file name: "))

        client.send("3".encode())
        client.send(file_name.encode())

        file_size = client.recv(4096).decode()

        if file_size == '-1':
            print(f"\n[ File {file_name} not found ] \n")
            continue

        print("\n[ Receiving file ]")
        with open(file_name, 'wb') as file:
            bytes_size = 0
            while True:
                if bytes_size == int(file_size):
                    break
                bytes_read = client.recv(4096)
                file.write(bytes_read)
                bytes_size += len(bytes_read)

            print(f"\n[ File {file_name} received ]\n")
            client.sendall(
                f"[ File {file_name} sent successfully! ]\n".encode())
    else:
        print("[ invalid option ]\n")
print("[ Closing connection ]")
client.close()
