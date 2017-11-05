#!/usr/bin/python
# Copyright 2017.
#
# Server usage:
#   ./stream.py -s | --serve <port>
# Server is run in a daemonized thread, while clients
# spawn a new thread; the server will not close
# and exit until all client threads are closed
#
# Client usage:
#   ./stream.py -c | --client -p | --port <port>
# Passing the -c flag will specify the file should
# be run as a client, and not a server daemon
import os
import sys
import threading
import logging

host = socket.gethostname() = 'localhost' # Local machine
buff = 1024 # Buffer size for data

def usage(stream):
   print('Usage: py ' + stream +
         ' [-h] | [--help]' +
         ' [-p] | [--port]' +  '<connect server port>' +
         ' [-l] | [--listen]' + ' <port number>' +
         ' [-c | --client] Create a client instance, defaults to server')

def send_message(port):
    """
    Connect to socket and send a message
    via the connection to any threads on the socket
    """
    sock = dial_socket(port=3033)
    sock.send(data.encode())
    sys.exit()

def request_file(port):
    """
    Connects to a socket and writes a
    file to another thread that requested it
    """
    sock = dial_socket(port=3033)
    print('Which file do you want?')
    sys.stdout.flush()
    data = sys.stdin.readline().rstrip()
    sock.send(data.encode())

    with condition:
        while not file_written:
            condition.wait()
        _write_file()

    def _write_file():
        f = open(resp, 'wb')
        while 1:
            print ("Receiving...")
            resp = conn.recv(1024)
            if not resp: break
            f.write(resp)
            f.close()
            print ("Done Receiving")
            break
    sys.exit()

def recieve_message(conn):
    """
    Listens to socket and returns
    any messages that are passed through it
    """
    conn = listen_socket(port=3033)
    data = conn.recv(1024)
    print('Message: {}'.format(data.decode()))

def file_response(conn):
    """
    Specify a file to recieve from a
    producer thread on the socket, and save
    the bytes that are return from it
    """
    conn = listen_socket(port=3033)
    while 1:
        req = conn.recv(1023)
        if not req: break
        resp = req.read(1024)
        while resp:
            print('Sending...')
            conn.send(resp)
        print('Done sending')
        conn.shutdown(socket.SHUT_WR)

def dial_socket(host='localhost', port):
    """
    Connect to the socket created by the
    server instance on specified host and port
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def listen_socket(host='localhost', port):
    """
    Create a socket and establish a perisistent
    connection to it, listening for events
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    # Initializes stream to socket
    # and returns that connection
    return conn

def exit(conn):
    """
    Close and exit the socket and script
    """
    conn.shutdown(socket.SHUT_WR)
    sys.exit(0)

def process(port):
    """
    Display client functions and spawn thread that
    handles the event chosen
    """
    actions = {'M': threading.Thread(target=send_message),
               'F': threading.Thread(target=request_file),
               'X': threading.Thread(target=exit)}
    while 1:
        print('Enter an option(\'m\', \'f\', \'x\'):')
        print('  (M)essage (send)')
        print('  (F)ile (request)')
        print(' e(X)it')
        event = sys.stdin.readline().rstrip().upper()
        actions[event]()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hscp:',
                                  ['help', 'serve', 'client', 'port='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    port = None
    client, server = False
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-p', '--port'):
            port = a
        # Take port value and start a server
        # daemon on that addres
        elif o in ('-s', '--serve'):
            server = True
            listen_socket(port)
        # Create a client, and process it
        # in order to connect to the socket
        # and transfer data
        elif o in ('-c', '--client'):
            client = True
            process(port)
        else:
            assert False, 'unhandled option'

if __name__ == "__main__":
    main()
