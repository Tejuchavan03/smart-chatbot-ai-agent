import nltk
import pickle
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download("punkt")

# ---------------- TRAINING DATA ----------------
questions = [
    "hello", "hi", "hey",
    "bye", "goodbye",
    "thank you", "thanks",
    "i am stressed", "i feel stressed", "i am sad",
    "help me", "can you help me"
]

labels = [
    "greeting", "greeting", "greeting",
    "farewell", "farewell",
    "thanks", "thanks",
    "stress", "stress", "stress",
    "help", "help"
]

# ---------------- MODEL ----------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

model = MultinomialNB()
model.fit(X, labels)

pickle.dump(model, open("chatbot_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

# ---------------- RESPONSES ----------------
responses = {
    "greeting": [
        "Hello! 😊 How can I help you?",
        "Hi! What can I do for you?"
    ],
    "farewell": [
        "Goodbye! Have a great day 😊",
        "Bye! Take care 👋"
    ],
    "thanks": [
        "You're welcome 😊",
        "Happy to help!"
    ],
    "stress": [
        "I'm sorry you're feeling stressed 😔",
        "Take a deep breath. I'm here for you 💙",
        "Do you want to talk about it?"
    ],
    "help": [
        "Sure! Tell me what you need help with 🙂",
        "I'm here to help you!"
    ],
    "unknown": [
        "I'm not sure I understand 🤔",
        "Can you explain a little more?",
        "I'm still learning 😊"
    ]
}

# ---------------- CHAT LOOP ----------------
print("Chatbot: Hello! Type 'exit' to quit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot: Bye 👋")
        break

    user_vec = vectorizer.transform([user_input])
    probs = model.predict_proba(user_vec)[0]
    confidence = max(probs)
    intent = model.predict(user_vec)[0]

    # Confidence check
    if confidence < 0.35:
        reply = random.choice(responses["unknown"])
    else:
        reply = random.choice(responses[intent])

    print("Chatbot:", reply)
import speech_recognition as sr
import pyttsx3
import nltk
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download("punkt")

# ---------------- SPEAK ----------------
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("Chatbot:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------- TRAINING DATA ----------------
sentences = [
    "hello", "hi", "hey",
    "bye", "goodbye",
    "thank you", "thanks",
    "i am stressed", "i am sad",
    "help me"
]

labels = [
    "greeting", "greeting", "greeting",
    "farewell", "farewell",
    "thanks", "thanks",
    "stress", "stress",
    "help"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(sentences)

model = MultinomialNB()
model.fit(X, labels)

# ---------------- KNOWLEDGE BASE ----------------
knowledge_answers = {
    "what is python": "Python is a programming language used for web development, data science, artificial intelligence, and automation.",
    "what is ai": "Artificial Intelligence is the ability of machines to think and learn like humans.",
    "what is machine learning": "Machine learning is a part of AI that allows systems to learn from data.",
    "what is your name": "I am a voice assistant created using Python.",
    "who are you": "I am a simple voice based AI assistant."
}



# ---------------- RESPONSES ----------------
responses = {
    "greeting": ["Hello! How can I help you?"],
    "farewell": ["Goodbye! Have a great day."],
    "thanks": ["You're welcome!"],
    "stress": [
        "I'm sorry you're feeling stressed.",
        "Take a deep breath. I'm here to listen."
    ],
    "help": ["Tell me what you want to know."],
    "unknown": [
        "I don't have information on that yet.",
        "Please ask something else."
    ]
}

# ---------------- LISTEN ----------------
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except:
        return ""

# ---------------- MAIN ----------------
speak("Hello, I am your voice assistant. Ask me a question.")

while True:
    user_input = listen()

    if user_input == "":
        speak("Please repeat.")
        continue

    if "exit" in user_input or "bye" in user_input:
        speak("Goodbye!")
        break

    # GOOGLE-LIKE KNOWLEDGE CHECK
    if user_input in knowledge_answers:
        speak(knowledge_answers[user_input])
        continue

    # ML INTENT
    user_vec = vectorizer.transform([user_input])
    probs = model.predict_proba(user_vec)[0]
    confidence = max(probs)
    intent = model.predict(user_vec)[0]

    if confidence < 0.4:
        speak(random.choice(responses["unknown"]))
    else:
        speak(random.choice(responses[intent]))