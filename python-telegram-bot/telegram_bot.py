import requests

from config import TELEGRAM_SEND_MESSAGE_URL

class TelegramBot:

    def __init__(self):
        """"
        Initializes an instance of the TelegramBot class.

        Attributes:
            chat_id:str: Chat ID of Telegram chat, used to identify which conversation outgoing messages should be send to.
            text:str: Text of Telegram chat
            first_name:str: First name of the user who sent the message
            last_name:str: Last name of the user who sent the message
        """

        self.chat_id = None
        self.text = None
        self.first_name = None
        self.last_name = None


    def parse_webhook_data(self, data):
        """
        Parses Telegram JSON request from webhook and sets fields for conditional actions

        Args:
            data:str: JSON string of data
        """

        message = data['message']

        self.chat_id = message['chat']['id']
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']
        self.last_name = message['from']['last_name']


    def action(self):
        """
        Conditional actions based on set webhook data.

        Returns:
            bool: True if the action was completed successfully else false
        """

        success = None
        data={}
        data['user_id']=self.chat_id
        data['question']=self.incoming_message_text
        data['session_id']='CLI-1025'
        data['projectId']='CA2020'
        data['overrides']={}
        data['overrides']['BOT_LIST']=[{'Icebreaker_bot': 'http://localhost:5130'},{'aiml_bot': 'http://localhost:5112'}, {'clarification_bot': 'http://localhost:5111'},{'ontology_bot': 'http://localhost:5001'},{'coherence_bot': 'http://localhost:5115'},{'evi': 'http://localhost:5117'},{'weather_bot': 'http://localhost:5118'}]
        data['overrides']['PRIORITY_BOTS']=['Icebreaker_bot','aiml_bot','clarification_bot','ontology_bot','coherence_bot','evi','weather_bot']
        r=requests.post(url='http://0.0.0.0:5000' , json=data)
        r.json()
        #print(r.json())
        self.outgoing_message_text = r.json()['result']
        success = self.send_message()
        return success


    def send_message(self):
        """
        Sends message to Telegram servers.
        """

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False
    

    @staticmethod
    def init_webhook(url):
        """
        Initializes the webhook

        Args:
            url:str: Provides the telegram server with a endpoint for webhook data
        """

        requests.get(url)


