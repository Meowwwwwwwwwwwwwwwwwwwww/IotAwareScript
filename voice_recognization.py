import speech_recognition as sr

def recognize_speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for speech
    
    try:
        # Recognize the speech using Google Speech API
        print("Recognizing speech...")
        command = recognizer.recognize_google(audio)  # Converts speech to text
        print(f"Recognized command: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Sorry, the speech service is unavailable.")
        return None
