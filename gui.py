import speech_recognition as sr
from compiler import compile_rule
from rules import map_command_to_dsl

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak your command.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results from the speech service.")
        return None

def main():
    print("Welcome to the IoT-Aware Script Compiler.")

    choice = input("Do you want to input the rule via voice? (y/n): ")

    if choice.lower() == 'y':
        command = recognize_speech()
        if command:
            mapped_command = map_command_to_dsl(command)
            result = compile_rule(mapped_command)
            print(f"Compiled result: {result}")
        else:
            print("No command recognized.")
    else:
        rule = input("Enter your automation rule: ")
        mapped_command = map_command_to_dsl(rule)
        result = compile_rule(mapped_command)
        print(f"Compiled result: {result}")

if __name__ == "__main__":
    main()
import speech_recognition as sr
from compiler import compile_rule
from rules import map_command_to_dsl

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak your command.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results from the speech service.")
        return None

def main():
    print("Welcome to the IoT-Aware Script Compiler.")

    choice = input("Do you want to input the rule via voice? (y/n): ")

    if choice.lower() == 'y':
        command = recognize_speech()
        if command:
            mapped_command = map_command_to_dsl(command)
            result = compile_rule(mapped_command)
            print(f"Compiled result: {result}")
        else:
            print("No command recognized.")
    else:
        rule = input("Enter your automation rule: ")
        mapped_command = map_command_to_dsl(rule)
        result = compile_rule(mapped_command)
        print(f"Compiled result: {result}")

if __name__ == "__main__":
    main()
