import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3  # Import Text-to-Speech engine

# Initialize TTS Engine
tts_engine = pyttsx3.init()

def speak_text(text):
    """Function to speak out the translated text."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def detect_language(text):
    """Detect if the input text is in Hindi or English."""
    for ch in text:
        if "\u0900" <= ch <= "\u097F":  # Hindi Unicode Range
            return "hi"  # Hindi
    return "en"  # English

def translate_speech():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        root.update_idletasks()
        
        try:
            audio = recognizer.listen(source, timeout=5)
            status_label.config(text="Recognizing...")

            # Convert speech to text
            detected_text = recognizer.recognize_google(audio, language="hi-en")  # Auto-detect Hindi/English
            status_label.config(text="Translating...")

            detected_lang = detect_language(detected_text)  # Detect if input is Hindi or English

            if detected_lang == "hi":
                translated_text = GoogleTranslator(source="hi", target="en").translate(detected_text)
            else:
                translated_text = GoogleTranslator(source="en", target="hi").translate(detected_text)

            # Display results
            input_textbox.delete("1.0", tk.END)
            input_textbox.insert(tk.END, detected_text)
            
            output_textbox.delete("1.0", tk.END)
            output_textbox.insert(tk.END, translated_text)
            
            status_label.config(text="Translation Complete ✅")

            # Speak out the translated text
            speak_text(translated_text)

        except sr.UnknownValueError:
            status_label.config(text="Could not understand the speech ❌")
        except sr.RequestError:
            status_label.config(text="Error connecting to Speech Recognition API ❌")

# Create GUI
root = tk.Tk()
root.title("Hindi-English Speech Translator")
root.geometry("500x450")
root.configure(bg="white")

title_label = tk.Label(root, text="Speech-to-Text Translator", font=("Arial", 14, "bold"), bg="white")
title_label.pack(pady=10)

input_textbox = scrolledtext.ScrolledText(root, height=3, width=50, wrap=tk.WORD)
input_textbox.pack(pady=5)

output_textbox = scrolledtext.ScrolledText(root, height=3, width=50, wrap=tk.WORD, bg="#e0f7fa")
output_textbox.pack(pady=5)

translate_button = tk.Button(root, text="Start Listening", font=("Arial", 12, "bold"), command=translate_speech, bg="green", fg="white")
translate_button.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 10), bg="white", fg="blue")
status_label.pack()

root.mainloop()
