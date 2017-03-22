import json

""" Format
{
'timestamp': <timestampt>,
 'sender': <username>,
 'response': <response>,
 'content': <content>,
 } 
 """
 #This is all assuming the server follows the requirements lined out in the project description, i.e no json objects within json objects, history being handled in a rational way by the server etc.
class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }
    def parse(self, payload):
        # decode the JSON object
        payload_dumped = json.loads(payload)
        if payload_dumped['response'] in self.possible_responses:
            return self.possible_responses[payload_dumped['response']](payload_dumped)
        else:
            return "[*] Error: Invalid response, Server fucked up"

    def parse_error(self, payload):
        return_string = str(payload['timestamp'])+': Error> '+str(payload['content'])
        return return_string
    
    def parse_info(self, payload):
        return_string = str(payload['timestamp'])+': '+str(payload['content'])
        return return_string
		
    def parse_message(self,payload):
        return_string = str(payload['timestamp'])+': '+str(payload['sender'])+'>'+str(payload['content'])
        return return_string

    def parse_history(self,payload):
        return_string = str(payload['timestamp'])+': Chat history>\n'
        for msg in payload['content']:
            return_string += self.parse_message(json.loads(msg)) + '\n'
        return return_string.rstrip()