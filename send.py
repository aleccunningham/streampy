#!/usr/bin/python

# Copyright 2017.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
