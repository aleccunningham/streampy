import threading
import os, sys

class fileRequestListener(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket= client_socket

    def run(self):
        filename = input('Which file do you want?')
        self.client_socket.send(filename.encode())
        from retrieve_file import RetrieveFile
        t = RetrieveFile(self.client_socket, filename)
        t.start()

        t.join()
        self.client_socket.close() # Close the connection
        os._exit(0)
