import datetime
import json
import os
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 160)

# Data storage
DATA_FILE = 'data.json'
data = {"notes": [], "todo": []}

# Speak function
def speak(text):
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

# Load existing data
def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Simple NLP - find keyword
def contains(text, keywords):
    return any(k in text for k in keywords)

# Generate response
def generate_response(user_input):
    user_input = user_input.lower()

    if contains(user_input, ["exit", "quit", "bye"]):
        return "Goodbye! Have a nice day.", True

    elif contains(user_input, ["your name", "who are you"]):
        return "I am AssistBot, your personal chatbot.", False

    elif contains(user_input, ["hello", "hi", "hey"]):
        return "Hello there! How can I help you today?", False

    elif contains(user_input, ["what can you do", "help", "features"]):
        tasks = [
            "1. Greet you",
            "2. Tell the current time and date",
            "3. Remember notes",
            "4. Show or clear notes",
            "5. Manage your to-do list",
            "6. Do simple math (like 2 + 3)",
            "7. Tell a joke",
            "8. (Mock) Weather update",
            "9. Exit"
        ]
        return "I can:\n" + "\n".join(tasks), False

    elif contains(user_input, ["time"]):
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {now}", False

    elif contains(user_input, ["date"]):
        today = datetime.date.today().strftime("%B %d, %Y")
        return f"Today's date is {today}", False

    elif contains(user_input, ["remember", "note this"]):
        speak("What should I remember?")
        note = input("You: ")
        if note:
            data['notes'].append(note)
            save_data()
            return f"I will remember: {note}", False
        return "I didn't get the note clearly.", False

    elif contains(user_input, ["what did you remember", "show notes"]):
        if data['notes']:
            return "Here are your notes:\n" + "\n".join(f"- {n}" for n in data['notes']), False
        return "You have no notes saved.", False

    elif contains(user_input, ["clear notes", "delete notes"]):
        data['notes'].clear()
        save_data()
        return "All notes have been cleared.", False

    elif contains(user_input, ["add task", "add to-do", "new task"]):
        speak("What task should I add?")
        task = input("You: ")
        if task:
            data['todo'].append(task)
            save_data()
            return f"Task added: {task}", False
        return "I didn't get the task clearly.", False

    elif contains(user_input, ["show list", "to-do", "tasks"]):
        if data['todo']:
            return "Here’s your to-do list:\n" + "\n".join(f"- {t}" for t in data['todo']), False
        return "Your to-do list is empty.", False

    elif contains(user_input, ["clear tasks", "clear list"]):
        data['todo'].clear()
        save_data()
        return "All to-do tasks cleared.", False

    elif contains(user_input, ["calculate", "+", "-", "*", "/"]):
        try:
            result = eval(user_input)
            return f"The answer is {result}", False
        except:
            return "Sorry, I couldn't calculate that.", False

    elif contains(user_input, ["joke"]):
        return "Why don't programmers like nature? It has too many bugs!", False

    elif contains(user_input, ["weather"]):
        return "It's sunny with a chance of AI takeover! (Just kidding 😄)", False

    else:
        return "Sorry, I didn't understand. Type 'help' to see what I can do.", False

# Chat loop
def chatbot():
    load_data()
    speak("Hi! I am AssistBot. Type something to begin.")

    while True:
        user_input = input("You: ")
        response, should_exit = generate_response(user_input)
        if response:
            speak(response)
        if should_exit:
            break

chatbot()
