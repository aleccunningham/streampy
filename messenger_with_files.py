#!/usr/bin/python
import sys
import socket
import getopt

def dial_socket(host='localhost', port):
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

def send_message(port):
    conn = dial_socket(port) # RecvMessages().start()
    while True:
        print('Enter your message:')
        sys.stdout.flush()
        message = sys.stdin.readline().rstrip()
        if not message: break
        try:
            conn.send(message.encode())
            break
        except:
            sys.exit()
    close(conn)

def send_file_request(port):
    conn = dial_socket(port)
    req = raw_input('Which file do you want?')
    conn.send(req.encode)
    close(conn)

def request_handler(port, req):
    conn = dial_socket(port)
    req = conn.recv(1024)
    with open(data, 'rb') as f:
        resp = f.read(1024)
    sock.send(resp)
    close(conn)

def close(conn):
    # Shutdown open socket connection
    conn.shutdown(socket.SHUT_WR)
    conn.close()

def process(command):
    actions = {
        'M': threading.Thread(target=send_message),
        'F': threading.Thread(target=request_file),
        'X': threading.Thread(target=close)}
    actions[command]()

def usage(script_name):
   print('Usage: py ' + script_name + '\n'
         '  [-l]  Listen on <port> for events\n' +
         '  [-s]  Connect to <port> as client\n' +
         '  [-p   <port>\n' )

#store command line argument
if __name__ == "__main__":
    # Handle file requests
    file_listen = threading.Thread(name='listener', target=request_handler)
    file_listen.setDaemon(True)
    file_listen.start()
    # Send messages over socket
    send_message = threading.Thread(name='send_message', target=send_message)
    # Send file to socket
    send_file = threading.Thread('send_file', target=send_file_request)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'lp:')
    except getopt.GetoptError as err:
        # print help information and exit:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-p', '--port'):
            port = a
        else:
            usage()
            sys.exit(2)

    while True:
        print('Enter an option(\'m\', \'f\', \'x\'):\n' +
              '  (M)essage (send)\n' +
              '  (F)ile (request)\n' +
              ' e(X)it')
        cmd = sys.stdin.readline().rstrip().upper()
        process(cmd)
        if option == 'M':
            send_message.start()
        elif option == 'F':
            send_file.start()
        else:

            close()
