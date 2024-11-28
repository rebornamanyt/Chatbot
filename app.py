import nltk
from nltk.chat.util import Chat, reflections
from flask import Flask, render_template, request
import google.generativeai as genai
import os
import logging

# Download necessary NLTK data
nltk.download('punkt')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Predefined responses
pairs = [
    [
        r"my name is (.*)|i am (.*)",
        ["Hello %1, How are you today?"]
    ],
    [
        r"thanks|thankyou",
        ["You'r Welcome"]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there!"]
    ],
    [
        r"what is your name?",
        ["My name is 'SYNAPSE'. I am a chatbot created by you."]
    ],
    [
        r"how are you?",
        ["I'm doing good. How about you?"]
    ],
    [
        r"sorry (.*)",
        ["It's alright.", "No problem."]
    ],
    [
        r"I am fine",
        ["Great to hear that!"]
    ],
    [
        r"quit|exit",
        ["Thanks for talking to me. I hope this was helpful to you!"]
    ],
    [
        r"good morning",
        ["Good morning! Hope you’re having a great day."]
    ],
    [
        r"good afternoon",
        ["Good afternoon! How’s your day going?"]
    ],
    [
        r"good evening",
        ["Good evening! What can I help you with tonight?"]
    ],
    [
        r"who created you?",
        ["I was created by the talented team at [LNCTU,BHOPAL]."]
    ],
]

chatbot = Chat(pairs, reflections)

# Google Gemini API key
os.environ["GEMINI_API_KEY"] = "AIzaSyBDasIOv14M0v6vKPjdLG9ZgKWdMPstRXw"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define the function to get Gemini response
def get_gemini_response(user_input):
    logging.info(f"Fetching response for: {user_input}")
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 150,
      "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
      model_name="gemini-1.5-pro",
      generation_config=generation_config,
    )
    
    chat_session = model.start_chat(
      history=[
      ]
    )
    
    response = chat_session.send_message(user_input)
    
    return response.text.strip()

# Flask app setup
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    try:
        logging.info(f"User input: {userText}")
        response = chatbot.respond(userText)
        if response:
            logging.info(f"Chatbot response: {response}")
            return str(response)
        else:
            logging.info("No predefined response, using Gemini API.")
            return get_gemini_response(userText)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return str(e)

if __name__ == "__main__":
    app.run()
