import pickle
import socket
import os

try:
    os.makedirs('./files')
except FileExistsError:
    pass

print("======== Server ========\n")

CLOSE_CONNECTION = '0'
STORE_FILE = '1'
RESPONSE_FILE_LIST = '2'
RESPONSE_FILE = '3'

HOST = "localhost"
PORT = 5050
ADDRESS = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDRESS)

print("[ Listening port ]\n")
server.listen(1)

print("[ Accepting connection ]\n")
conn, addr = server.accept()

print("[ Connected ]\n")

while 1:
    op = conn.recv(1024).decode()

    if op == CLOSE_CONNECTION:
        break
    elif op == STORE_FILE:
        file_name = conn.recv(1024).decode()
        file_size = conn.recv(4096).decode()

        print("[ Receiving file ]\n")

        with open(os.path.join("./files", file_name), 'wb') as file:
            bytes_size = 0
            while True:
                if bytes_size == int(file_size):
                    break
                bytes_read = conn.recv(4096)
                file.write(bytes_read)
                bytes_size += len(bytes_read)
            print("[ File uploaded ]\n")
            conn.sendall(
                f"[ File {file_name} successfully uploaded! ]\n".encode())
    elif op == RESPONSE_FILE_LIST:
        conn.send(pickle.dumps(os.listdir('./files')))
        print("[ List of files sent ]\n")
        print(conn.recv(1024).decode())
    elif op == RESPONSE_FILE:
        file_name = conn.recv(1024).decode()

        try:
            with open(os.path.join("./files", file_name), 'rb') as file:
                print(f"[ Sending file ]\n")
                conn.send(
                    str(os.path.getsize(os.path.join("./files", file_name))).encode())
                while True:
                    bytes_read = file.read()
                    if not bytes_read:
                        break
                    conn.sendall(bytes_read)
                print(conn.recv(1024).decode())
        except FileNotFoundError:
            print(f"[ File {file_name} not found ] \n")
            conn.send('-1'.encode())
print("[ Closing connection ]")
conn.close()
