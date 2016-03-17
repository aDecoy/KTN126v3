import json

class MessageParser():
    def __init__(self, client):

        self.client = client

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
            'names': self.parse_names
        }


    def parse(self, json_string, catch=None):
        #Decode the JSON object
<<<<<<< HEAD
        payload = json.loads(json_string)
=======
       # payload = json.loads(json_string.decode('utf-8'))
        payload = json.loads(json_string)

>>>>>>> origin/master
        print(payload)
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            raise ValueError('Response not valid')

    def parse_error(self, payload):
        return payload['content']

    def parse_info(self, payload):
        if payload['content'] == "Login successful":
            self.client_logged_in = True
        elif payload['content'] == "Logout successful":
            self.client_logged_in = False
        return payload['content']

    def parse_message(self, payload):
        return payload['sender'] + ": " + payload['content']

    def parse_names(self, payload):
        names = payload['content']
        nameList = "Users in lobby:" + "\n"
        for name in names:
            nameList += name + "\n"
        return nameList

    def parse_history(self, payload):
        json_list = json.loads(payload['content'])
        history = ""
        for item in json_list:
            history += self.parse_message(item) + "\n"
        return history

    # Include more methods for handling the different responses...
