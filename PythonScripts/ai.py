#build 2 way commnicate with c#
import pyttsx3
import speech_recognition as sr

class AI:
    __name = "Anton"
    __skill = []

    def __init__(self, name=None):
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty("rate", 150)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        name = ('Anton')
        print(name)
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        
        if name is not None:
            self.__name = name
        
        print("Listening")
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)  # Adjust for ambient noise for 0.5 seconds

    

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        sentence = "Hello, my name is" + self.__name
        self.__name = value
        self.engine.say(sentence)
        self.engine.runAndWait()
    
    def say(self, sentence):
        self.engine.say(sentence)
        self.engine.runAndWait()
    
    def listen(self):
        print("Say Something")
        with self.m as source:
            audio = self.r.listen(source, timeout=5, phrase_time_limit=5)
        print("Got it")
        try:
            phrase = self.r.recognize_google(audio, show_all=False, language="en_US")
            self.engine.run
        except  :
            self.engine.runAndWait()
        print("You Said", phrase)
        return phrase
    





