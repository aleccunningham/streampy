import os, sys, threading

class Message(threading.Thread):
    """
    Parse a message sent from a client to
    the server and close the socket when finished
    """
    def __init__(self, conn, data, daemon=True):
        self.conn = conn
        self.data = data
        return super(Message, self).__init__(conn, data)

    def run(self, conn=None, data=None):
        # Listen for events occuring
        # on the connection to the socket
        listenForConnection()
        f = open(self.data, 'wb')
        while 1:
            print ("Receiving...")
            data = conn.recv(1024)
            if not data: break
            f.write(data)
            f.close()
            print ("Done Receiving")
            break
        conn.close() # Close the connection
        os._exit(0)


class File(threading.Thread):
    """
    Parse a file sent from a client to
    the server and close the socket when finished
    """
    def __init__(self, conn, data, daemon=True):
        self.conn = conn
        self.data = data
        return super(File, self).__init__(conn, data)

    def run(self, conn, data=None):
        connectToServer()
        f = open(self.data, 'wb')
        while 1:
            print ("Receiving...")
            data = conn.recv(1024)
            if not data: break
            f.write(data)
            f.close()
            print ("Done Receiving")
            break
        conn.close() # Close the connection
        os._exit(0)
