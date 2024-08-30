#################################################################################################################
# Name:-        Kunj Shah
# Project:-     Jarvis
# Description:- This project, named Jarvis, is a voice-activated assistant built using Python. It leverages the 
#               pyttsx3 library for text-to-speech capabilities and speech_recognition for converting speech to 
#               text. The application can execute various commands, such as performing web searches, opening 
#               websites, and finding locations on maps. The user interface is created with Tkinter, featuring a 
#               button that activates voice recognition when clicked. The assistant also maintains a history of 
#               recognized commands in a text file for future reference.
#################################################################################################################

# Various imports
import pyttsx3
import speech_recognition as sr
import webbrowser
import tkinter as tk
import threading
import requests

# Adds History to a text file
def history(text):
    print("Adding to History")
    with open("history.txt", "a") as file:
        file.write(text + "\n")

# Variables for Tkinter
root = tk.Tk()
btn = tk.Button(root, text="Activate Jarvis")

# Global variable to keep track if "Jarvis" has been recognized
activated = False

# Creates and returns a Recognizer
def initializeRecognizer():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
    return recognizer

# Listens to the Audio and uses various methods to send to website
def speechToText(recognizer):
    print("Listening...")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        data = recognizer.recognize_google(audio)
        print("Taking you to the web...")
        command(data)
    except sr.UnknownValueError:
        textToSpeech("We are not able to recognize what you said")
    resetUI()

# SAYS what you want it to say
def textToSpeech(text):
    engine = pyttsx3.init()
    engine.say(text)
    print(text)
    engine.runAndWait()

# Some of the standard commands
def command(cmd):
    URL = None
    if "search" in cmd:
        text = cmd.replace("search", "").strip()
        textToWeb(text)
    elif "open" in cmd:
        text = cmd.replace("open", "").strip()
        URL = f"https://www.{text.replace(' ', '')}.com"
    elif "on map" in cmd:
        text = cmd.replace("on map", "").strip()
        URL = f"https://www.google.co.in/maps/search/{text.replace(' ', '+')}/"
    else:
        textToWeb(cmd)
    if URL:
        webbrowser.open(URL)

def get_youtube_video_id(query):
    api_key = "youtubeAPI.json"  # replace with your YouTube API key
    url = f"https://www.googleapis.com/youtube/v3/search?part=id&q={query}&type=video&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["items"]:
        return data["items"][0]["id"]["videoId"]
    return None

# When you say "Hello", only then it goes ahead or else ACCESS DENIED
def scrtKey(recognizer):
    global activated
    if not activated:
        textToSpeech("What is your name?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            data = recognizer.recognize_google(audio)
            if "hello" in data:
                print("Recognizing...")
                textToSpeech("Welcome Sir! How can I help you?")
                activated = True
                speechToText(initializeRecognizer())
            else:
                print("Access Denied")
                scrtKey(initializeRecognizer())
        except sr.UnknownValueError:
            textToSpeech("We are not able to recognize what you said")

# Takes the text and opens URL
def textToWeb(text):
    URL = f"https://google.com/search?q={text.replace(' ', '+')}"
    webbrowser.open(URL)

# Changes the Window just after clicking the button
def eventOcc(event):
    root.configure(bg='white')
    btn.configure(bg='black', fg='white', text='Activated')
    threading.Thread(target=scrtKey, args=(initializeRecognizer(),)).start()

# Resets UI elements back to default
def resetUI():
    root.configure(bg='black')
    btn.configure(bg='white', fg='black', text='Activate Jarvis')

# Opens the window with a button
def window():
    root.geometry("400x400")
    root.resizable(False, False)
    root.configure(bg='black')

    btn.place(width=100, height=50, x=200, y=200, anchor=tk.CENTER)
    btn.configure(bg='white')
    btn.bind("<Button-1>", eventOcc)

    tk.mainloop()

# The driver method
def driver():
    window()

# runs driver
driver()
