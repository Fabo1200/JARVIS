import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests

wolf_app_id = "ADD_YOURS_HERE"


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')


def get_volume():
    volume = engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
    return volume


def set_volume(vol):
    engine.setProperty('volume', vol)  # setting up volume level  between 0 and 1


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif 12 <= hour < 18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")


def take_command():
    r = sr.Recognizer()
    r.energy_threshold = 3000

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            input_statement = r.recognize_google(audio, language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e_tc:
            print(f"e_tc:  {e_tc}\n")
            speak("Pardon me, please say that again")
            return "None"
        return input_statement


def take_command_word():
    r = sr.Recognizer()
    r.energy_threshold = 2500

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            input_statement = r.recognize_google(audio, language='en-in')
            print(f"user said:{input_statement}\n")

        except Exception as e_tcw:
            print(f"e_tcw:  {e_tcw}\n")
            return "None"
        return input_statement


print('Loading - JARVIS')
speak('Loading - JARVIS')
wish_me()
delay = 2

if __name__ == '__main__':

    while True:
        statement = take_command_word().lower()

        if "goodbye" in statement or "ok bye" in statement or "stop" in statement:
            speak('JARVIS is shutting down,Good bye')
            print('JARVIS is shutting down,Good bye')
            break

        if "jarvis" in statement or "hey jarvis" in statement or "hey" in statement \
                or "computer" in statement or "hi" in statement or "hello" in statement:

            speak("Tell me how can I help you?")
            statement = take_command().lower()

            if statement == 0:
                continue

            if "goodbye" in statement or "ok bye" in statement or "stop" in statement:
                speak('JARVIS is shutting down,Good bye')
                print('JARVIS is shutting down,Good bye')
                break

            if 'wikipedia' in statement:
                speak('Searching Wikipedia...')
                try:
                    statement = statement.replace("wikipedia", "")
                    results = wikipedia.summary(statement, sentences=3)

                except Exception as e_wik:
                    print(f"e_wik:  {e_wik}\n")
                    speak("Request was unclear! Please repeat")
                    statement = take_command().lower()
                    results = wikipedia.summary(statement, sentences=3)

                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in statement:
                webbrowser.open_new_tab("https://www.youtube.com")
                speak("youtube is open now")
                time.sleep(delay)

            elif 'open google' in statement:
                webbrowser.open_new_tab("https://www.google.com")
                speak("Google chrome is open now")
                time.sleep(delay)

            elif 'open gmail' in statement:
                webbrowser.open_new_tab("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox")
                speak("Google Mail open now")
                time.sleep(delay)

            elif "weather" in statement:
                api_key = "ADD_YOURS_HERE"
                base_url = "https://api.openweathermap.org/data/2.5/weather?"
                speak("whats the city name")
                city_name = take_command()
                complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                response = requests.get(complete_url)
                x = response.json()
                if x["cod"] != "404":
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_temperature_celsius = current_temperature - 273.15
                    current_humidity = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    speak(" Temperature is " +
                          str(int(current_temperature_celsius)) + " Degrees Celsius "
                          "\n humidity in percentage is " +
                          str(current_humidity) +
                          "\n description  " +
                          str(weather_description))
                    print(" Temperature is " +
                          str(int(current_temperature_celsius)) + " Degrees Celsius "
                          "\n humidity (in percentage) = " +
                          str(current_humidity) +
                          "\n description = " +
                          str(weather_description))

                else:
                    speak(" City Not Found ")

            elif 'time' in statement:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"the time is {strTime}")

            elif 'who are you' in statement or 'what can you do' in statement:
                speak('I am JARVIS your personal assistant. I can open youtube, google chrome, gmail and stackoverflow,'
                      'tell you the time, take a photo, search wikipedia, give you weather forecasts globally,'
                      'open the NYT, you can ask me mathematical or geographical questions')

            elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
                speak("I was built by Fabian Staegemann")
                print("I was built by Fabian Staegemann")

            elif "open stackoverflow" in statement:
                webbrowser.open_new_tab("https://stackoverflow.com/login")
                speak("Here is stackoverflow")

            elif 'news' in statement:
                news = webbrowser.open_new_tab("https://www.nytimes.com/")
                speak('Here are some headlines from the New York Times ,Happy reading')
                time.sleep(delay)

            elif "camera" in statement or "take a photo" in statement:
                ec.capture(0, "robo camera", "img.jpg")

            elif 'search' in statement:
                statement = statement.replace("search", "")
                webbrowser.open_new_tab(statement)
                time.sleep(delay)

            elif 'ask' in statement:
                speak('What question do you want me to answer')
                question = take_command()
                app_id = wolf_app_id
                client = wolframalpha.Client(wolf_app_id)
                res = client.query(question)
                answer = next(res.results).text
                speak(answer)
                print(answer)

            elif "log off" in statement or "sign out" in statement:
                speak("Ok, your pc will log off in 10 sec make sure you exit from all applications")
                subprocess.call(["shutdown", "/l"])

time.sleep(delay)
