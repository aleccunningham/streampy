import os, sys, threading

class Message(threading.Thread):
    """
    Send a string via client to the
    server to be decoded and returned
    """
    def __init__(self, sock, data):
        self.sock = sock
        self.data = data
        return super(Message, self).__init__(sock, data)

    def run(self, sock, data):
        connectToServer()
        _get_data(sock)
        sys.stdout.flush()
        sock.send(data.encode())
        sys.exit()

    def _get_data(self, sock):
        print('Enter your message:')
        sys.stdout.flush()
        data = sys.stdin.readline().rstrip()
        if not data: break
        return data


class File(threading.Thread):

    def __init__(self, sock, data):
        self.sock = sock
        self.data = data
        return super(File, self).__init__(sock, data)

    def run(self, conn):
        connectToServer()
        _get_data(conn)
        sock.send(data.encode())
        sys.exit()

    def _get_data(self, conn):
        print('Which file do you want?')
        sys.stdout.flush()
        data = sys.stdin.readline().rstrip()
        if not data: break
        return data
