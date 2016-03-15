# -*- coding: utf-8 -*-
import socket
import datetime
import json
from Client.MessageParser import MessageParser
from Client.MessageReceiver import MessageReceiver



class ClientKlassen:
    """
    This is the chat client class
    """
    host=""
    server_port=1
    messageParser=MessageParser
    username="ikke logget inn"

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
        self.host=host
        self.server_port=server_port

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code

        messagereciveer=MessageReceiver(self,self.connection)
        messageParser =  MessageParser(self)

        self.run()

    def run(self):
        # Initiate the connection to the server
        print(self.host,self.server_port)
        self.connection.connect((self.host, self.server_port))
        print("connected!!!!")
        print("skriv inn: login <username>")



        while True:
            user_input=input()
            print(user_input)
            tid=str(datetime.datetime.utcnow())
            if (self.username=="ikke logget inn"):
                if (user_input=='hjelp' or user_input=='help'):
                   # self.connection.send(bytes("{ 'timestamp': '"+tid+"' 'sender': 'None' 'request': 'help' 'content': 'None'", 'utf-8'))
                   # self.connection.send(bytes("{ 'timestamp': '"+tid+"' 'sender': 'None' 'request': 'help' 'content': 'None'}",'utf-8'))

                if (user_input.startswith("login")):
                    rygsekk=user_input.split()
                    self.username=rygsekk[1]
                    self.connection.send(bytes("{ 'timestamp':'"+tid +"' 'sender': '"+self.username+"' 'request': 'login' 'content':'"+rygsekk[1]+"'}",'utf-8'))
            else:

                if (user_input=="help"):
                    self.connection.send(bytes("{ 'timestamp':'"+tid +"' 'sender': '"+self.username+"' 'request': 'help' 'content':'None'}",'utf-8'))

                if (user_input=="names"):
                    self.connection.send(bytes("{ 'timestamp':'"+tid +"' 'sender': '"+self.username+"' 'request': 'names' 'content':'None'}",'utf-8'))


                if (user_input.startswith("login")):
                    rygsekk=user_input.split()
                    self.username=rygsekk[1]
                    self.connection.send(bytes("{ 'timestamp':'"+tid +"' 'sender': '"+self.username+"' 'request': 'login' 'content':'"+rygsekk[1]+"'}",'utf-8'))

                if (user_input=="logout"):
                    self.connection.send(bytes("{ 'timestamp':'"+tid+"' 'sender': '"+self.username+"' 'request': 'logout' 'content':'None'}",'utf-8'))
                else:
                    self.connection.send(bytes("{ 'timestamp':'"+tid +"' 'sender': '"+self.username+"' 'request': 'msg' 'content':'"+user_input+"'}",'utf-8'))




    def disconnect(self):
        self.connection.close()
        print("closed")
        pass

    def receive_message(self, message):
       # print(message)
        self.send_payload(message)
        pass

    def send_payload(self, data):
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
