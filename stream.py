#!/usr/bin/python
import sys, socket, getopt, fileinput
from send import Message, File
from recieve import Message, File

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

host = socket.gethostname() = 'localhost' # Local machine
buff = 1024 # Buffer size for data

def usage(stream):
   print('Usage: py ' + stream +
         ' [-l] | [--listen]' + ' <port number>' +
         ' [-p] | [--port]' +  '<connect server port>' +
         ' [-c] Create a client instance, defaults to server')

def serve(host='localhost', port=3033):
    """
    Specifying a port, starts a server that
    spawns daemonized threads listening for
    strings or bytes on port
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    # Initializes stream to socket
    return conn

def process():
    _connect()
    while True:
        print('Enter an option(\'m\', \'f\', \'x\'):')
        print('  (M)essage (send)')
        print('  (F)ile (request)')
        print(' e(X)it')
        option = sys.stdin.readline().rstrip().upper()

        if option == 'M':
            data = sys.stdin.readline().rstrip()
            send.Message(data).start()
        if option == 'F':
            data = sys.stdin.readline().rstrip()
            send.File(data).start()
        if option == 'X':
            shutdown(conn)

def shutdown(conn):
    """
    Connect to the socket and close it
    along with any established connections
    """
    _connect()
    print('Closing your sockets... goodbye')
    conn.shutdown(sock.SHUT_RDWR)
    conn.close()

def _connect(host='localhost', port=3033):
    """
    Connect to the socket created by the
    server instance on specified host and port
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def main():
    """
    Parse arguments; set either a server or client
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:sc',
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
            serve(port)
        # Create a client, and process it
        # in order to connect to the socket
        # and transfer data
        elif o in ('-c', '--client'):
            client = True
            process(port)
        else:
            assert False, 'unhandled option'

#store command line argument
if __name__ == "__main__":
    main()
