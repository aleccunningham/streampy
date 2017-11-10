import threading
import os, sys

class RetrieveFile(threading.Thread):
    def __init__(self, client_socket, data):
        threading.Thread.__init__(self)
        self.client_socket= client_socket
        self.data = data

    def run(self):
        data = self.client_socket.recv(1024)
        if os.path.isfile(file_name):
            with open(data, 'rb') as f:
                send_bytes = f.read(1024)
                self.client_socket.send(send_bytes)
                while send_bytes != "":
                    send_bytes = f.read(1024)
                    self.client_socket.send(send_bytes)
        else:
            break

        f.close()
        self.client_socket.close() # Close the connection
        os._exit(0)
