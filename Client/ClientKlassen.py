# -*- coding: utf-8 -*-
import socket
import json
from Client.MessageParser import MessageParser


class ClientKlassen:
    """
    This is the chat client class
    """
    host=""
    server_port=1
    messageParser=MessageParser()

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
        self.host=host
        self.server_port=server_port

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code


        #msg =  MessageParser()

        self.run()

    def run(self):
        # Initiate the connection to the server
        print(self.host,self.server_port)
        self.connection.connect((self.host, self.server_port))
        print("connected!!!!")

        while True:
            user_input==input()
            if (user_input=="disconect"):
                self.disconnect()
            if user_input


    def disconnect(self):
        self.connection.close()
        print("closed")
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        print(message)
        self.send_payload(message)
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        print(self.messageParser.parse(data))
        pass
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = ClientKlassen('127.0.0.1', 9998)
