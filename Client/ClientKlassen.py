# -*- coding: utf-8 -*-
import socket
import datetime
import json
from MessageParser import MessageParser
from MessageReceiver import MessageReceiver
import threading

#from Client.MessageParser import MessageParser
#from Client.MessageReceiver import MessageReceiver

class ClientKlassen:
    """
    This is the chat client class
    """
    host=""
    server_port=1
    messageParser=MessageParser
    messagereceiver = MessageReceiver
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

        self.messagereceiver = MessageReceiver(self,self.connection)
        self.messageParser =  MessageParser(self)

        self.run()

    def run(self):
        # Initiate the connection to the server
        print(self.host,self.server_port)
        self.connection.connect((self.host, self.server_port))
        print("connected!!!!")
        print("skriv inn: login <username>")

        def send_json(time,sender,request,content):
            package = json.dumps({ "timestamp": time, "sender": sender , "request": request ,"content": content })
            self.connection.send(package)

        t = threading.Thread(target=self.messagereceiver.run)
        t.start()

        while True:
            user_input = raw_input()
            #user_input = input()       #python 3
            tid=str(datetime.datetime.utcnow())
            if (self.username=="ikke logget inn"):
                if (user_input=="close"):
                     self.disconnect()

                if (user_input=='hjelp' or user_input=='help'):
                   # self.connection.send(bytes('{ "content": "None" }', 'utf-8'))
                    send_json(tid,"None","help" ,"None")

                if (user_input.startswith("login")):

                    rygsekk=user_input.split()
                    if (user_input.count(" ")>0):
                        self.username=rygsekk[1]
                        send_json(tid,self.username,"login",rygsekk[1])
            else:

                if (user_input=="help"):
                    send_json(tid,self.username,"help","None")

                elif (user_input=="names"):
                    send_json(tid,self.username,"names","None")

                elif (user_input=="logout"):
                    send_json(tid,self.username,"logout","None")
                    self.username="ikke logget inn"


                elif (user_input=="close"):
                    self.disconnect()


                else:
                    send_json(tid,self.username,"msg",user_input)




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
    client = ClientKlassen('78.91.24.143', 9998)
