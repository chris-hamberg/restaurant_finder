import speech_recognition as sr
import sys

def to_text(query='Speak...'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #TODO: Replace with Computer Generated Voice 
        print(query)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        if text == 'quit' or text == 'exit': sys.exit(0)
        print(text)
        return text

        #print(r.recognize_google(audio, key=GOOGLE_SPEECH_RECOGNITION_API_KEY))
    except sr.UnknownValueError:
        print('Not understood')
    except sr.RequestError as e:
        print('Bad request: {e}'.format_map(vars()))

if __name__ == '__main__':
    while True:
        to_text()
