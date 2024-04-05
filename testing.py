import speech_recognition as sr
import ollama

def transcribe_speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Set pause threshold for a faster response to speech
    recognizer.pause_threshold = 0.2  # Extremely responsive
    # Ensure non_speaking_duration is less than or equal to pause_threshold
    recognizer.non_speaking_duration = 0.1

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        # Listen for a short period to calibrate the energy threshold for ambient noise levels
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Calibrated. Please speak.")

        # Capture the audio
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google's speech recognition
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            # Error: recognizer could not understand the audio
            return None
        except sr.RequestError as e:
            # Error: could not request results from Google's speech recognition service
            return None

def ollama_response(input_text):
    
    response = ollama.chat(model='tinydolphin', messages=[
        {
            'role': 'user',
            'content': input_text,
        },
    ])
    return response['message']['content']
    

if __name__ == "__main__":
    text = transcribe_speech()
    if text!="":
        response = ollama_response(text)
        print(response)