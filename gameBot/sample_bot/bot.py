import logging
import random
from argparse import ArgumentParser
import json
import os
from flask import Flask, request
from flask_restful import Api
from utils import log
from utils.abstract_classes import Bot
from utils.dict_query import DictQuery
from datetime import datetime
import random
import aiml
import csv

from test_rasa_interface import send

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("AIML/std-startup.xml")
kernel.respond("load aiml b")

FFG_questions = []
with open("AIML/family_fortune_questions.csv", newline='') as csvfile:
    FFG = csv.reader(csvfile, delimiter=';')
    for row in FFG:
        FFG_questions.append(row)

print(FFG_questions[1][1])
FFG_NO_QUESTIONS = len(FFG_questions)




print(FFG_NO_QUESTIONS)
app = Flask(__name__)
api = Api(app)
BOT_NAME = "triviaBot"
#VERSION = log.get_short_git_version()
#BRANCH = log.get_git_branch()


logger = logging.getLogger(__name__)

parser = ArgumentParser()
parser.add_argument('-p', "--port", type=int, default=5130)
parser.add_argument('-l', '--logfile', type=str, default='logs/' + BOT_NAME + '.log')
parser.add_argument('-cv', '--console-verbosity', default='info', help='Console logging verbosity')
parser.add_argument('-fv', '--file-verbosity', default='debug', help='File logging verbosity')

class LastLetterGame():
    last_letter = "a"
    words_used = []
    turn = 0
    bot_turn = True
    confirming_word = False
    answer = ""
    game_explained = False
    ask_question = False

    def __init__(self):
        pass

    def LastLetterGame_manager(self, user_utterance, intent):
        response = ""
        if self.turn is 0:
            response = kernel.respond("LLGGAMENAME") + " "

        if "explain_game" in intent["intent"]["name"].lower():
            self.game_explained = False
        if self.ask_question is True and self.game_explained is False:
            if "affirm" in intent["intent"]["name"].lower():
                self.game_explained = True
                self.ask_question = False

        if self.game_explained is False:
            self.ask_question = True
            response += kernel.respond("LLGEXPLAINGAME")
            return response


        if "repeat_word" in intent["intent"]["name"].lower():
            response = self.repeat_last_word()
            return response

        elif self.turn == 0:
            response = self.start_LLG()

        elif  "answer_question" in intent["intent"]["name"].lower() or "affirm" in intent["intent"]["name"].lower() or "deny" in intent["intent"]["name"].lower():
            response = self.get_word(user_utterance, intent)

        else:
            response = kernel.respond("LLGDIDNOTGETTHAT")

        self.turn += 1
        return response

    def get_word(self,user_utterance, intent):
        # parse answer

        if self.confirming_word is False:
            if len(intent["entities"]) > 0:
                self.answer = intent["entities"][0]["value"]
                print("entity: " + self.answer)
            else:
                return kernel.respond("LLGDIDNOTGETTHAT")



        # confirm answer
        if self.confirming_word is False:
            self.confirming_word = True
            return kernel.respond("LLGCONFIRMANSWER " + self.answer)

        elif self.confirming_word is True:
            # posative response
            self.confirming_word = False
            if "affirm" in intent["intent"]["name"].lower():
                return self.get_response_last_letter_game()
            elif "answer_question" in intent["intent"]["name"].lower():
                if self.answer.lower() in intent["entities"][0]["value"]:
                    return self.get_response_last_letter_game()
            else:
                return kernel.respond("LLGNOTFINALWORD " + self.last_letter[0])

    def get_response_last_letter_game(self):
        # the 'result' member is intended as the actual response of the bot
        # self.response.result = random.choice(self.greetings)
        #check if correct answer
        if self.answer[0].lower() != self.last_letter[0].lower():
            # wrong answer
            letters = self.last_letter[0] + " LLGWRONGANSWER " + self.answer
            return kernel.respond(letters) + " " + kernel.respond("LLGTRYAGAIN")

        else:
            output = self.answer[-1] * 3
            print(output)
            word = kernel.respond(output)
            print(word)
            if word in self.words_used:

                return kernel.respond("LLGYOUWIN " + self.last_letter[0])

            else:
                self.last_letter = word[-1]
                self.words_used.append(word)
                response = kernel.respond("LLGMYWORDIS " + word)

                # print(input)
                return response

    def repeat_last_word(self):
        if len(self.words_used) > 0:
            return kernel.respond("LLGLASTWORDWAS " + self.words_used[-1])
        else:
            return "we have not started yet"

    def start_LLG(self):
        letters = ("a","b","c","d","e","f","g","i","p")
        start_letter = random.choice(letters)
        word = kernel.respond(start_letter * 3)
        print(word)
        self.words_used.clear()
        self.words_used.append(word)
        self.last_letter = word[-1]
        response = kernel.respond("LLGSTART " + word)
        print(response)
        return response


class FamilyFortuneGame():
    question_asked = False
    game_explained = False
    final_comment = ""
    question_text = ""
    current_question_index = 0
    possible_answers = []
    def FFG_manager(self, user_utterance, intent):
        #user_utterance = request_data.get("current_state.state.nlu.annotations.processed_text")
        if self.game_explained is False:
            return self.explain_game()

        if self.question_asked is False:
            self.get_new_question()
            self.question_asked = True
            return self.ask_question()
        else:
            return self.check_answer(user_utterance)

    def get_new_question(self):
        self.possible_answers.clear()
        i = random.randint(0, FFG_NO_QUESTIONS)
        self.question_asked = True
        self.current_question_index = i
        question = FFG_questions[i]
        #set question text
        self.question_text = question[0]
        print(self.question_text)
        #set final comment
        if question[-1].upper() != "NULL":
            self.final_comment = question[-1]
        else:
            self.final_comment = ""
        #get possible answers
        for x in range(1, len(question)-1, 2):
            if "/" in question[x]: #if their are variants of an answer (driving car, driving van)
                alist = question[x].split('/')
                self.possible_answers.append(alist)
            else:
                self.possible_answers.append(question[x])

    def ask_question(self):
        output = kernel.respond("FFGASKQUESTION " + self.question_text)
        return output

    def explain_game(self):
        output = kernel.respond("FFGEXPLAIN")
        self.game_explained = True
        return output

    def check_answer(self, answer):
        for i in range(0,len(self.possible_answers)):
            ans = self.possible_answers[i]
            print(ans)
            if isinstance(ans, list) is True:
                for x in ans:
                    if self.are_same(x,answer) is True:
                        return self.correct_answer(answer, i)
            else:
                if self.are_same(ans, answer) is True:
                    return self.correct_answer(answer, i)
        return "wrong"


    def correct_answer(self,answer,index):
        self.question_asked = False
        rank = ("number one","second","third", "fourth", "fifth", "sixth", "seventh", "eighth")
        output = kernel.respond(answer + " FFGCORRECT " + rank[index])
        output += ". "
        output += kernel.respond("FFGCONTINUE")

        return output

    def are_same(self,given_ans, correct_ans):
        if given_ans.upper() == correct_ans.upper():
            return True
        else:
            return False

class GameManager():
    last_letter_game = True
    trivia_game = False
    family_fortune_game = False


    def manager(self, user_utterance, intent):

        if "ffg_ans_question" in intent["intent"]["name"].lower():
            if len(intent["entities"]) > 0:
                self.answer = intent["entities"][0]["value"]
                print("ffg entity: " + self.answer)

        if "stop_talking" in intent["intent"]["name"].lower():
            return kernel.respond("STOPTALKING")

        if "stop_game" in intent["intent"]["name"].lower():
            return "you will play this game untill the ice is broken"

        if self.last_letter_game is True:
            return LLG.LastLetterGame_manager(user_utterance, intent)
        elif self.family_fortune_game is True:
            return FFG.FFG_manager(user_utterance, intent)
        else:
            i = random.randint(0,2)
            if i < 1:
                self.last_letter_game = False
                self.trivia_game = False
                self.family_fortune_game = True
            else:
                self.last_letter_game = True
                self.trivia_game = False
                self.family_fortune_game = False
            return "lets play a game"




LLG = LastLetterGame()
FFG = FamilyFortuneGame()
Manager = GameManager()

class GreetingsBot(Bot):


    def __init__(self, **kwargs):
        # Warning: the init method will be called every time before the post() method
        # Don't use it to initialise or load files.
        # We will use kwargs to specify already initialised objects that are required to the bot
        super(GreetingsBot, self).__init__(bot_name=BOT_NAME)



    def get(self):
        pass

    def post(self):
        # This method will be executed for every POST request received by the server on the
        # "/" endpoint (see below 'add_resource')

        # We assume that the body of the incoming request is formatted as JSON (i.e., its Content-Type is JSON)
        # We parse the JSON content and we obtain a dictionary object
        request_data = request.get_json(force=True)

        # We wrap the resulting dictionary in a custom object that allows data access via dot-notation
        request_data = DictQuery(request_data)

        # We extract several information from the state
        user_utterance = request_data.get("current_state.state.nlu.annotations.processed_text")
        intent = send(user_utterance)

        print("intent: " + intent["intent"]["name"])
        last_bot = request_data.get("current_state.state.last_bot")

        logger.info("------- Turn info ----------")
        logger.info("User utterance: {}".format(user_utterance))
        logger.info("Last bot: {}".format(last_bot))
        logger.info("---------------------------")


        output = Manager.manager(user_utterance, intent)
        print(output)
        self.response.result = output

        # we store in the dictionary 'bot_params' the current time. Remember that this information will be stored
        # in the database only if the bot is selected
        self.response.bot_params["time"] = str(datetime.now())

        # The response generated by the bot is always considered as a list (we allow a bot to generate multiple response
        # objects for the same turn). Here we create a singleton list with the response in JSON format
        return [self.response.toJSON()]





if __name__ == "__main__":
    args = parser.parse_args()
    
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    log.set_logger_params(BOT_NAME + '-', logfile=args.logfile,
                          file_level=args.file_verbosity, console_level=args.console_verbosity)

    api.add_resource(GreetingsBot, "/")

    app.run(host="0.0.0.0", port=args.port)
