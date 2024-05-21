import socket
import time

client_sockets = []

HOST = socket.gethostbyname(socket.gethostname())
print(HOST)
PORT = 9999

print('>> Server Start with ip :', HOST)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))

server_socket.listen()

print('echo server start')

client_soc, addr = server_socket.accept()
print('connected client addr:', addr)
data = client_soc.recv(100)
msg = data.decode()
print('recv msg:', msg)
client_soc.sendall(msg.encode(encoding='utf-8'))

time.sleep(5)
server_socket.close()