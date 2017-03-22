# -*- coding: utf-8 -*-
import SocketServer, json
from time import time, asctime, sleep
from threading import Thread
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
history = []
users = {}
class ClientHandler(SocketServer.BaseRequestHandler):
    global messages
    global users
    global messages_history
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    def handle(self):
        """
        This method handles the connection between a client and the server.
        """

        self.loggedin = False
        self.username = ""
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            print "[*] Received: "+str(received_string)

            recv = json.loads(received_string)

            request = recv['request']
            content = recv['content']
            #If your request is not here, go away.
            if request == 'login':
                self.handle_login(content)
            elif request == 'logout':
                self.handle_logout()
            elif request == 'msg':
                self.handle_msg(content)
            elif request == 'names':
                self.handle_names()
            elif request == 'help':
                self.handle_help()
            elif request == 'history':
                self.handle_history()
            else:
               self.handle_error('Command not recognized')

    def handle_login(self,user):	
        if not user.isalnum():
            self.handle_error('Invalid username')
            return
			
        if self.loggedin:
            self.handle_error('Already a logged in user on this connection')
            return
			
        if user in users:
            self.handle_error('Username taken')
            return

        self.username = user
        users[user] = self.connection
        self.loggedin = True
        payload = {'timestamp':asctime(),'sender':'server','response':'info','content':'Logged in as ' + user}
        self.send(payload, self.connection)


    def handle_logout(self):
        if not self.loggedin:
            self.handle_error('Not logged in')
            return
        
        self.loggedin = False
        del users[self.username]
        payload = {'timestamp':asctime(),'sender':self.username,'response':'info','content':'Logged out.'}
        self.send(payload, self.connection)

    def handle_msg(self,message):
        if not message:
            self.handle_error('Invalid message')
            return
			
        if not self.loggedin:
            self.handle_error('User not logged in')
            return
        
        payload = {'timestamp':asctime(),'sender':self.username,'response':'message','content':message}
        history.append(json.dumps(payload))
        for user, connection in users.iteritems():
            self.send(payload, connection)
		

    def handle_names(self):
        if not self.loggedin:
            self.handle_error('User not logged in')
            return
			
        content = ", ".join(users.keys())
        payload = {'timestamp':asctime(),'sender':'server','response':'info','content':content}
        self.send(payload, self.connection)


    def handle_history(self):
        if not self.loggedin:
            self.handle_error('User not logged in')
            return
			
        #content = "\n".join(history)
        payload = {'timestamp':asctime(),'sender':'server','response':'history','content':history}
        self.send(payload, self.connection)

    def handle_error(self, error):
        payload = {'timestamp':asctime(),'sender':'server','response':'error','content':error}
        self.send(payload, self.connection)


    def handle_help(self):
        content = "Help: \n Commands: login, logout, msg, names, history. \n Usage: command + content"
        payload = {'timestamp':asctime(),'sender':'server','response':'info','content':content}
        self.send(payload, self.connection)

    def send(self, data, connection):
        connection.sendall(json.dumps(data))

        # TODO: Add handling of received payload from client



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print '[*] Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
