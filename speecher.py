import speech_recognition as sr
import pyttsx
from os import system
import os
import sqlite3
import random
import thread

class Speecher(object):

    def __init__(self, connection):
        self.r = sr.Recognizer()
        self.connection = connection
        self.lastmessage = None
        self.st = False

        #thread.start_new_thread( self.small_talk , ())

    def small_talk(self):
        while 1 == 1:
            if random.randrange(0, 10000000) == 0 and self.st == True:
                conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '/brain.db')
                c = conn.cursor()
                c.execute("SELECT output FROM messages")
                answers = c.fetchall()
                if len(answers) > 0:
                    ans = answers[random.randrange(0, len(answers))][0]
                    system('say ' + ans)
                    self.lastmessage = ans

    def listen(self):
        if self.lastmessage == None:
            system('say hello')
            self.lastmessage = 'hello'

        with sr.Microphone() as source:
                audio = self.r.listen(source)

        try:    

            user_text = self.r.recognize(audio)
            my_text = self.answer(user_text.replace("'", ''))

            self.st = False
            system('say ' + my_text)

            self.learn(self.lastmessage.replace("'", ''), user_text.replace("'", ''))

            self.lastmessage = my_text
            self.st = True
            self.listen()
        except LookupError: 
                system('say ' + 'vad sa du?')
                self.lastmessage = 'vad sa du?'
                self.listen()

    def learn(self, input, output):
        c = self.connection.cursor()
        c.execute('INSERT INTO messages (input, output) VALUES("'+input+'", "'+output+'")')
        self.connection.commit()

    def answer(self, input):
        c = self.connection.cursor()

        c.execute("SELECT output FROM messages WHERE input LIKE '%"+input+"%'")
        answers = c.fetchall()

        if len(answers) > 0:
            return answers[random.randrange(0, len(answers))][0]

        perfect_answers = []
        bad_answers = []
        
        c.execute("SELECT output FROM messages")
        answers = c.fetchall()


        if len(answers) == 0:
            return 'sorry?'
        else:
            for ans in answers:
                if ans[0].find(input) > 0 or ans[0] == input:
                    perfect_answers.append(ans[0])

            if len(perfect_answers) == 0:
                for ans in answers:
                    for word in input.split(' '):
                        if ans[0].find(word) > 0 and random.randrange(0, 3) == 0:
                            bad_answers.append(ans[0])


        if len(perfect_answers) > 0:
            return perfect_answers[random.randrange(0, len(perfect_answers))]

        else:
                if len(bad_answers) > 0:
                    return bad_answers[random.randrange(0, len(bad_answers))]
                else:
                    return 'what?'


