import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
    # Loop in case of errors
    while(1):
        try:
            # use the microphone as source for input
            with sr.Microphone() as source2:
                # Prepare recognizer to recive input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = r.recognize_google(audio2)

                return MyText
        
        except sr.UnknownValueError as e:
            print("Speech recognition could not understand audio: {0}".format(e))
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service: {0}".format(e))


        
    return

def output_text(text):
    f = open('output.txt','a')
    f.write(text)
    f.write('\n')
    f.close()
    return

while(1):
    text = record_text()
    output_text(text)

    print('Wrote text')