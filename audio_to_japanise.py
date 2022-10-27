import speech_recognition as sr
import os


OUTPUT_PATH   = "./output.wav"


r = sr.Recognizer()


with sr.AudioFile(OUTPUT_PATH) as source:
    audio = r.record(source)

print(audio)
text = r.recognize_google(audio, language='ja-JP')


print(text)
