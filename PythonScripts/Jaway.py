import pyjokes
import wikipedia
from ai import AI
from todo import Todo, Item
from weather import Weather
from datetime import datetime
from calendar_skill import Calendar_skill
import dateparser
import socket
import requests
import random

calendar = Calendar_skill()
calendar.load()
jaway = AI()
todo = Todo()

def joke():
    funny = pyjokes.get_joke()
    print(funny)
    jaway.say("Here is your favorite joke: " + funny)

def weather():
    myweather = Weather()
    forecast = myweather.forecast
    jaway.say(forecast)

def add_todo() -> bool:
    item = Item()
    jaway.say("Tell me what to add to the list")
    try:
        item.title = jaway.listen()
        todo.new_item(item)
        message = "Added " + item.title
        jaway.say(message)
        return True
    except Exception as e:
        print(f"Oops, there was an error: {e}")
        return False

def wiki_1(command) -> bool:
    try:
        question = command.replace('who', '').strip()
        answer = wikipedia.summary(question, sentences=1)
        jaway.say(answer)
        print(answer)
        return True
    except Exception as e:
        print(f"Can you ask again? Error: {e}")
        return False

def wiki_2(command) -> bool:
    try:
        question = command.replace("what", '').strip()
        answer = wikipedia.summary(question, sentences=1)
        jaway.say(answer)
        print(answer)
        return True
    except Exception as e:
        print(f"Can you ask again? Error: {e}")
        return False

def list_todos():
    if len(todo.items) > 0:
        jaway.say("Here are your to-do's")
        for item in todo.items:
            jaway.say(item.title)
    else:
        jaway.say("The to-do list is empty!")

def remove_todo() -> bool:
    jaway.say("Tell me which item to remove")
    try:
        item_title = jaway.listen()
        todo.remove_item(title=item_title)
        message = "Removed " + item_title
        jaway.say(message)
        return True
    except Exception as e:
        print(f"Oops, there was an error: {e}")
        return False

def add_event() -> bool:
    jaway.say("What is the name of the event?")
    try:
        event_name = jaway.listen()
        jaway.say("When is this event?")
        event_begin = jaway.listen()
        event_isodate = dateparser.parse(event_begin).strftime("%Y-%m-%d %H:%M:%S")
        jaway.say("What is the event description?")
        event_description = jaway.listen()
        message = "Ok, adding event: " + event_name
        jaway.say(message)
        calendar.add_event(begin=event_isodate, name=event_name, description=event_description)
        calendar.save()
        return True
    except Exception as e:
        print(f"Oops, there was an error: {e}")
        return False

def remove_event() -> bool:
    jaway.say("What is the name of the event you want to remove?")
    try:
        event_name = jaway.listen()
        try:
            calendar.remove_event(event_name=event_name)
            jaway.say("Event removed successfully")
            calendar.save()
            return True
        except Exception as e:
            jaway.say(f"Sorry, I could not find the event: {event_name}. Error: {e}")
            return False
    except Exception as e:
        print(f"Oops, there was an error: {e}")
        return False

def send_message_to_unity(message):
    try:
        host = '127.0.0.1'  # Unity server IP
        port = 8080         # Unity server port

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(message.encode('utf-8'))
            print(f"Message '{message}' sent to Unity.")
    except Exception as e:
        print(f"Failed to send message: {e}")


def TrigerrandomAction1():
    if random.randint(1,50)==1:
        send_message_to_unity("Triger Action 1")
    else:
        print("skip")
    


def list_events(period):
    try:
        this_period = calendar.list_events(period=period)
        if this_period is not None:
            message = "There "
            message += 'are ' if len(this_period) > 1 else 'is '
            message += str(len(this_period))
            message += ' events' if len(this_period) > 1 else ' event'
            print(message)
            jaway.say(message)
            for event in this_period:
                event_date = event.begin.datetime
                weekday = datetime.strftime(event_date, "%A")
                day = str(event_date.day)
                month = datetime.strftime(event_date, "%B")
                year = datetime.strftime(event_date, "%Y")
                message = f"On {weekday} {day} of {month} {year}"
                print(message)
                jaway.say(message)
                name = event.name
                message = "There is an event called " + name
                jaway.say(message)
                description = event.description
                message = "The event description is " + description
                print(description)
                jaway.say(message)
        else:
            jaway.say("There are no events in this period.")
    except Exception as e:
        print(f"Oops, there was an error: {e}")

wake = "Anton"
jaway.say("Hello my name is Anton")
command = ""
if __name__ == "__main__":
    while True:
        try:
            TrigerrandomAction1()
            command = jaway.listen()
            if wake in command:
                TrigerrandomAction1()
                jaway.say("how can i help")
                command = jaway.listen()
                if "what" in command:
                    wiki_2(command)
                elif "who" in command:
                    wiki_1(command)
                elif 'joke' in command:
                    joke()
                elif 'add' in command:
                    add_todo()
                elif "to do" in command:
                    list_todos()
                elif "remove" in command:
                    remove_todo()
                elif "weather" in command:
                    weather()
                elif command in ["good morning", "good afternoon", "good evening"]:
                    now = datetime.now()
                    hr = now.hour
                    if 0 <= hr < 12:
                        message = "Morning"
                    elif 12 <= hr < 17:
                        message = "Afternoon"
                    elif 17 <= hr < 21:
                        message = "Evening"
                    else:
                        message = "Night"
                    message = "Good " + message + "!"
                    jaway.say(message)
                    weather()
                    list_todos()
                elif command in ['add event', 'add to calendar', 'new event', 'add a new event']:
                    add_event()
                elif command in ['delete event', 'remove event', 'cancel event']:
                    remove_event()
                elif command in ['list events', "what's on this month", "what's coming up this month"]:
                    list_events(period='this month')
                elif command in ["what's on this week", "what's coming up this week"]:
                    list_events(period='this week')
                elif command in ['event']:
                    list_events(period='all')
        except:
            print(f"Oops, there was an error")
