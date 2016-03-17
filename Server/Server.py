# -*- coding: utf-8 -*-

import SocketServer #ServerSocket is all lower case in Python 3
import datetime
import json
import time


"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

history = []
users = {}
username = ""
info = "info"
server_send = "Server"
error = "error"

class ClientHandler(SocketServer.BaseRequestHandler): #ServerSocket is all lower case in Python 3
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    def send_all(self,time,sender,response,content):
        json_object = json.dumps({"timestamp" : time, "sender" : sender, "response" : response, "content" : content})
        for user in users.itervalues():
            #if user != self:
            user.connection.send(json_object)

    def send_self(self,time,sender,response,content):
        json_object = json.dumps({"timestamp" : time, "sender" : sender, "response" : response, "content" : content})
        self.connection.send(json_object)

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        sender = None
        response_type = None
        response_message = None

        # Loop that listens for messages from the client
        while True:

            received_json = self.connection.recv(4096)
            #Access the dictionary insode the JSON object to get the dictionary
            message = json.loads(received_json)
            #Get the time the server recieves the message
            # Needs to be configured to a better format
            now = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") #use datetime.now() in Pyhton 3

            #If it is a login request
            if message["request"] == "login":
                print("Recieved a login request")
                #Adds the content of the login message as username
                username = message.get("content")

                #If the user is already in the dictionary of users, send error
                if (self in users.itervalues()):
                    print("Trying to create user: %s, but they are already logged in" %username)
                    response_message = "The user %s is already logged in" %username
                    self.send_self(now,server_send,error,response_message)

                #If username is already taken, send error
                elif (username in users):
                    print("Trying to create user: %s, but the username is already taken" %username)
                    response_message = "The Username %s is already in use by someone else" %username
                    self.send_self(now,server_send,error,response_message)

                #if the dictionary doesn't contain the user
                elif (username not in users):
                    print("Creating user: %s" %username)
                    #add the user to the dictonary
                    users[username] = self
                    #message is a standard login message
                    response_message = "%s just logged in to the chat room" %username
                    #sends response to all
                    self.send_all(now,sender,info,response_message)
                    #sends back the previous history to the user if the history exists
                    if (len(history) > 0):
                        self.send_self(now,sender,"history",history)

                else:
                    response_message = "Something went wrong with the login process"
                    self.send_self(now,server_send,error,response_message)

            #If it is a logout request
            elif message.get("request") == "logout":
                print("Recieved a logout request")
                #if the dictionary of users contains the user
                if (self in users.itervalues()):
                    print("Logging out user: %s" %username)
                    response_message = "Logged out user: %s" %username
                    #delete user from dictionary
                    del users[username]
                    #send logout message to all
                    self.send_all(now,sender,info,response_message)

                #If logged in user isn't logged in (failsafe):
                else:
                    print("Tried to log out user that is not logged in: %s" %username)
                    response_message = "User is not logged in, and thus cannot log out, which makes no sense.."
                    self.send_self(now,server_send,error,response_message)

            #If it is a request to send a message
            elif message.get("request") == "msg":
                print("Recieved msg request")
                #If the sender is a logged in user in the dictionary
                if (self in users.itervalues()):
                    print("User %s is sending a message to everyone" %username)
                    sender = username
                    response_type = "message"
                    #To broadcast the users message to all other users, the content will be forwarded
                    response_message = message["content"]
                    #Add the message to history list as a JSON object
                    history.append(json.dumps({ "timestamp" : now, "sender": sender, "response": response_type, "content": response_message }))
                    #Send the message to everyone in the chat room
                    self.send_all(now,sender,response_type,response_message)

                #If the user is not logged in, send error message
                else:
                    print("Message request failed")
                    response_message = "You are not currently logged in"
                    self.send_self(now,server_send,error,response_message)

            #If the request is for user info
            elif message.get("request") == "names":
                print("Names request sent by %s" %username)
                response_message = "Users currently logged in: \n"
                #cycle through the keys (usernames) in the users dictionary
                for key in users.keys():
                    #adds every name (key) to a string
                    response_message += key + "\n"
                self.send_self(now,server_send,info,response_message)

            elif message.get("request") == "help":
                print("Help request sent by %s" %username)
                #Help is not filled out, didn't have time to fill it out right now..
                response_message = "There should be a help string here"
                self.send_self(now,server_send,info,response_message)

            #If the request doesn't match any of the preset types, send error
            else:
                print ("Request form %s was not of correct type" %username)
                response_message = "Request type seems to not be valid"
                self.send_self(now,server_send,error,response_message)

        self.connection.close()

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer): #ServerSocket is all lower case in Python 3
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
    HOST, PORT = '0.0.0.0', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
