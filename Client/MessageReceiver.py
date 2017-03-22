# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        #Basically, this is magic.
        Thread.__init__(self)
        self.connection = connection
        # Flag to run thread as a deamon
        self.daemon = True
        self.client = client
        # TODO: Finish initialization of MessageReceiver
        
    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while True:
            msg = self.connection.recv(4096)
            if msg:
                self.client.receive_message(msg)
