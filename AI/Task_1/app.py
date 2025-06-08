import datetime
import json
import os
import pyttsx3
import speech_recognition as sr
import difflib

# Initialize text-to-speech
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 160)

# Data storage
DATA_FILE = 'data.json'
data = {
    "notes": [],
    "todo": []
}

# Load existing data
def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Speak output
def speak(text):
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

# Listen from mic
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        return r.recognize_google(audio).lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that. Please type it.")
        return input("You: ").lower()
    except sr.RequestError:
        speak("Voice recognition not available. Please type.")
        return input("You: ").lower()

# Find intent using fuzzy match
def intent_match(user_input, possible_phrases, cutoff=0.6):
    matches = difflib.get_close_matches(user_input, possible_phrases, n=1, cutoff=cutoff)
    return matches[0] if matches else None

# Possible actions
intents = {
    "greeting": ["hi", "hello", "hey"],
    "bye": ["bye", "exit", "quit"],
    "name": ["your name", "who are you", "what is your name"],
    "menu": ["menu", "help"],
    "features": ["what can you do", "your features", "what do you do"],
    "get_time": ["what time", "current time", "tell me time"],
    "get_date": ["what date", "current date", "today date"],
    "remember_note": ["remember", "note this", "save note"],
    "show_notes": ["what did you remember", "show notes", "recall notes"],
    "add_task": ["add to-do", "add task", "add to list", "new task"],
    "show_tasks": ["show list", "to-do list", "show tasks", "my tasks"],
    "clear_notes": ["clear notes", "delete all notes"],
    "clear_tasks": ["clear list", "clear tasks", "reset to-do"]
}

def detect_intent(user_input):
    for intent, phrases in intents.items():
        if any(p in user_input for p in phrases):
            return intent
        match = intent_match(user_input, phrases)
        if match:
            return intent
    return None

# Show menu
def show_menu():
    speak("I can help you remember notes, manage your to-do list, and tell you the time or date.")

# Main response generator
def generate_response(user_input):
    intent = detect_intent(user_input)

    if intent == "greeting":
        return "Hello! How can I assist you?", False

    if intent == "bye":
        return "Goodbye! Take care.", True

    if intent == "name":
        return "I am AssistBot, your personal assistant.", False

    if intent == "menu":
        show_menu()
        return "", False

    if intent == "features":
        return "I can manage your to-do list, remember notes, and tell you the time or date.", False

    if intent == "get_time":
        return "The time is " + datetime.datetime.now().strftime("%I:%M %p"), False

    if intent == "get_date":
        return "Today's date is " + datetime.date.today().strftime("%B %d, %Y"), False

    if intent == "remember_note":
        speak("What would you like me to remember?")
        note = listen()
        if note:
            data['notes'].append(note)
            save_data()
            return f"I'll remember that: {note}", False
        return "I didn't get the note clearly.", False

    if intent == "show_notes":
        if data['notes']:
            return "Here’s what I remember:\n" + "\n".join(f"- {n}" for n in data['notes']), False
        return "I don’t have any notes yet.", False

    if intent == "add_task":
        speak("What task should I add to your list?")
        task = listen()
        if task:
            data['todo'].append(task)
            save_data()
            return f"Added task: {task}", False
        return "I didn't get the task clearly.", False

    if intent == "show_tasks":
        if data['todo']:
            return "Here’s your to-do list:\n" + "\n".join(f"- {t}" for t in data['todo']), False
        return "Your to-do list is empty.", False

    if intent == "clear_notes":
        data['notes'].clear()
        save_data()
        return "All notes cleared.", False

    if intent == "clear_tasks":
        data['todo'].clear()
        save_data()
        return "To-do list cleared.", False

    return "I’m not sure how to help with that. Say 'menu' for help.", False

# Main chatbot loop
def chatbot():
    load_data()
    speak("Hi! I am AssistBot. How can I help you today?")
    show_menu()

    while True:
        user_input = listen()
        response, should_exit = generate_response(user_input)
        if response:
            speak(response)
        if should_exit:
            break

chatbot()
