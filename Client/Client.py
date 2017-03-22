# -*- coding: utf-8 -*-
import socket, json, time
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        self.host = host
        self.server_port = server_port
        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        listener = MessageReceiver(self,self.connection)
        listener.daemon = True
        listener.start()
        self.get_input()
        
    def disconnect(self):
        self.connection.close()

    def receive_message(self, message):
        parser = MessageParser()
        print parser.parse(message)

    def send_payload(self, input):
        input_list = input.split(" ", 1)
        if(len(input_list) == 1):
            content = None
        else:
			content = input_list[1]
		
        request = input_list[0]
        request = request.lower()
        payload = {'request':request, 'content':content}
        payload_json = json.dumps(payload)

        self.connection.send(payload_json)


    def get_input(self):
        while True:
            input = str(raw_input("> "))
            self.send_payload(input)
            time.sleep(0.1)


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
