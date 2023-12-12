import socket

class TCPClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.server_ip, self.server_port))

    def send_message(self, message):
        self.client_socket.sendall(bytes(message))

    def receive_response(self, buffer_size=2000):
        return self.client_socket.recv(buffer_size).decode("UTF-8").split(" ")

    def close_connection(self):
        self.client_socket.close()
