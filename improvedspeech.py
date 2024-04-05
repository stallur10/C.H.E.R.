import speech_recognition as sr

def listen_and_transcribe():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        # Adjust for ambient noise and set a higher energy threshold
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold += 200  # Increase based on ambient noise level
        print("Set minimum energy threshold to {}".format(recognizer.energy_threshold))

    # Lower the pause_threshold to be more responsive to end of speech in noisy environments
    recognizer.pause_threshold = 0.5

    while True:  # Loop indefinitely
        print("\nListening for speech... Speak now!")
        with microphone as source:
            try:
                # Listen for the first phrase and extract it into audio data
                audio = recognizer.listen(source, timeout=5)
                print("Processing speech...")
                # Recognize speech using Google Speech Recognition
                text = recognizer.recognize_google(audio)
                print("You said: " + text)
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")
                continue  # Go back to the start of the loop and listen again
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    listen_and_transcribe()
