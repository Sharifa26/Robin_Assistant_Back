from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

app = Flask(__name__)

# Text-to-Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)


# Function to make the assistant speak
def talk(text):
    engine.say(text)
    engine.runAndWait()


# Function to take voice command
def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
            return command
        except Exception:
            return "Sorry, I couldn't understand that."


# Function to process commands
def run_alexa(command):
    response = ""
    if 'play' in command:
        song = command.replace('play', '').strip()
        response = f"Playing {song} on YouTube"
        pywhatkit.playonyt(song)
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        response = f"The current time is {current_time}"
    elif 'who is' in command or 'what is' in command:
        query = command.replace('who is', '').replace('what is', '').strip()
        info = wikipedia.summary(query, sentences=2)
        response = info
    elif 'joke' in command:
        response = pyjokes.get_joke()
    elif 'are you single' in command:
        response = "I am in a relationship with Wi-Fi."
    elif 'date' in command:
        response = "Sorry, I have a headache!"
    else:
        response = "I didn't understand. Please say the command again."
    
    talk(response)
    return response


# API Endpoint
@app.route("/run", methods=["POST"])
def run_voice_assistant():
    data = request.get_json()
    command = data.get("command", "")
    response = run_alexa(command)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
