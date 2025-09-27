# Install dependency:
# pip install SpeechRecognition sounddevice numpy

import sounddevice as sd
import numpy as np
import speech_recognition as sr
import time

# Duration and sampling rate
DURATION = 5  # seconds per recording
SAMPLERATE = 16000

# Initialize recognizer
recognizer = sr.Recognizer()

def recognize_speech():
    print("Recording your voice...")
    
    # Record audio
    audio = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='float32')
    sd.wait()
    audio_array = audio.flatten()
    
    # Convert NumPy array to bytes for SpeechRecognition
    audio_data = (audio_array * 32768).astype(np.int16).tobytes()
    audio_sr = sr.AudioData(audio_data, SAMPLERATE, 2)  # 2 bytes per sample
    
    # Recognize speech
    try:
        text = recognizer.recognize_google(audio_sr)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

# Continuous loop
while True:
    recognize_speech()
    time.sleep(1)  # wait 1 second before next recording
