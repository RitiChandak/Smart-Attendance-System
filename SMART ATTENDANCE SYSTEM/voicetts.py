import pyttsx3

def text_to_speech(text, rate):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)  # Adjust speed here
    engine.say(text)
    engine.runAndWait()





if __name__ == "__main__":
    message = "RIYA Have a nice day!"
    text_to_speech(message, rate=130)  # Adjust rate as needed, 100 is a reasonable starting point
