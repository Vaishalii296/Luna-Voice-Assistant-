import tkinter as tk
from tkinter import scrolledtext, PhotoImage
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import pyjokes
import webbrowser
import threading
from PIL import ImageGrab
import time
import comtypes
import atexit
comtypes.CoInitialize()

# Assistant engine
engine = pyttsx3.init()
atexit.register(lambda: engine.stop())

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 = male, 1 = female
engine.setProperty('rate', 150)

def speak(text):
    def update_gui():
        output_box.insert(tk.END, f"\n🧠 Assistant: {text}\n")
        output_box.see(tk.END)
    root.after(0, update_gui)  # Schedule GUI update on the main thread
    engine.say(text)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        command = command.lower()
        print(f"You said: {command}")

        if 'luna' in command:
            # Remove 'luna' from command to get actual action
            command = command.replace('luna', '').strip()
            output_box.insert(tk.END, f"\n🎙️ You: {command}")
            output_box.see(tk.END)
            return command
        else:
            speak("Say 'Luna' to activate me.")
            return ""
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Network error.")
    return ""

def take_screenshot():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    path = f"./{filename}"  # Save in project folder (or customize path)
    img = ImageGrab.grab()
    img.save(path)
    speak(f"Screenshot taken and saved as {filename}")

def handle_command(command):
    if 'play' in command:
        song = command.replace('play', '')
        speak(f'Playing {song}')
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f'Current time is {time}')

    elif 'who is' in command:
        person = command.replace('who is', '')
        try:
            info = wikipedia.summary(person, sentences=5)
            speak(info)
        except:
            speak("Couldn't find information.")
    
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif 'exit' in command or 'stop' in command:
        speak("Goodbye!")
        try:
            root.quit()
        except:
            pass

    elif 'screenshot' in command or 'screen shot' in command:
        take_screenshot()

    else:
        speak("Sorry, I don't understand that yet.")

def start_assistant():
    def run():
        time.sleep(1)
        speak("Hello! I am Luna. Say my name to begin.")
        while True:
            command = take_command()
            if command:
                handle_command(command)
                if 'exit' in command or 'stop' in command:
                    break
    threading.Thread(target=run).start()

# GUI setup
root = tk.Tk()
root.title("💖 Luna - Your Assistant")
root.geometry("700x500")
root.configure(bg="#FFF0F5")  # Soft lavender blush

# Optional image/logo
try:
    logo = PhotoImage(file="assets/mic-24.png")  # Replace with cute icon if available
    logo = logo.subsample(4, 4)
    img_label = tk.Label(root, image=logo, bg="#FFF0F5")
    img_label.pack(pady=10)
except:
    pass

title = tk.Label(root, text="✨ Luna - Your Assistant ✨", font=("Comic Sans MS", 22, "bold"),
                 fg="#C71585", bg="#FFF0F5")
title.pack()

start_button = tk.Button(root, text="🎤 Start Listening", font=("Comic Sans MS", 14, "bold"),
                         bg="#FFB6C1", fg="white", padx=20, pady=5, command=start_assistant,
                         activebackground="#FF69B4", activeforeground="white")
start_button.pack(pady=10)

exit_button = tk.Button(root, text="🚪 Exit", font=("Comic Sans MS", 12),
                        bg="#FFC0CB", fg="white", command=lambda: [speak("Goodbye!"), root.quit()])
exit_button.pack(pady=5)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15,
                                       font=("Georgia", 11), bg="#FAE6FA", fg="#4B0082")
output_box.pack(padx=10, pady=10)

footer = tk.Label(root, text="🎐 Made by Vaishali Rajput • B.Tech CSE 🎐",
                  font=("Comic Sans MS", 9), bg="#FFF0F5", fg="#DB7093")
footer.pack(pady=5)

try:
    root.mainloop()
except KeyboardInterrupt:
    try:
        speak("Closing Luna. Goodbye!")
        root.quit()
    except:
        pass
