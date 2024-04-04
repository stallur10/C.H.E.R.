import speech_recognition as sr
import pyttsx3
import datetime
import ollama

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
    # Loop in case of errors
    while True:
        try:
            # use the microphone as source for input
            with sr.Microphone() as source2:
                # listens for the user's input
                print("Listening...")
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                print("You said:", MyText)
                return MyText

        except sr.UnknownValueError as e:
            print("Speech recognition could not understand audio: {0}".format(e))
            return "hello"
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service: {0}".format(e))
            return "hello"
def ollama_response(input_text):
    response = ollama.chat(model='llama2', messages=[
        {
            'role': 'user',
            'content': input_text,
        },
    ])
    print(response['message']['content'])
    return response

def output_text(text):
    print("Ollama's Response:", text)
    return

while True:
    text = record_text()
    response = ollama_response(text)
    output_text(response)
