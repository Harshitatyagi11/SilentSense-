# Install dependencies:
# pip install sounddevice numpy transformers torch SpeechRecognition

import sounddevice as sd
import numpy as np
from transformers import pipeline
import speech_recognition as sr
import time
import socket  # For ESP32 Wi-Fi communication

# ESP32 IP aur port
ESP32_IP = "192.168.23.241"
ESP32_PORT = 8888

# Zero-shot audio classification model
classifier = pipeline(
    task="zero-shot-audio-classification",
    model="laion/clap-htsat-unfused"
)

# Target classes
candidate_labels = ["siren", "doorbell", "alarm", "crying", "dog barking"]

# Thresholds
CONFIDENCE_THRESHOLD = 0.8  # Audio classification confidence
AMPLITUDE_THRESHOLD = 0.03  # Minimum loudness to consider
DURATION = 5  # seconds per recording
SAMPLERATE = 16000

# Speech recognizer
recognizer = sr.Recognizer()

# Function to send message to ESP32
def send_to_esp32(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ESP32_IP, ESP32_PORT))
        sock.sendall((message + "\n").encode())
        sock.close()
    except Exception as e:
        print("ESP32 not reachable:", e)

# Main function: speech first, then sound
def detect_audio():
    print("Recording audio...")
    
    # Record audio
    audio = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='float32')
    sd.wait()
    audio_array = audio.flatten()
    
    # Ignore very quiet audio
    if np.max(np.abs(audio_array)) < AMPLITUDE_THRESHOLD:
        print("Too quiet, ignoring...")
        return
    
    # --- Speech Recognition First ---
    try:
        audio_data = (audio_array * 32768).astype(np.int16).tobytes()
        audio_sr = sr.AudioData(audio_data, SAMPLERATE, 2)
        text = recognizer.recognize_google(audio_sr)
        if text.strip() != "":
            print("Detected speech:", text)
            send_to_esp32(text)
            return  # Speech detected, skip sound classification
    except sr.UnknownValueError:
        pass  # Speech not recognized, try sound classification
    except sr.RequestError as e:
        print("Speech recognition request failed:", e)
    
    # --- Sound Classification if no speech detected ---
    results = classifier(audio_array, sampling_rate=SAMPLERATE, candidate_labels=candidate_labels)
    top = max(results, key=lambda x: x['score'])
    
    if top['score'] >= CONFIDENCE_THRESHOLD:
        detected = f"Detected sound: {top['label']} ({top['score']:.2f})"
        print(detected)
        send_to_esp32(top['label'])
    else:
        print("No clear sound or speech detected.")

# Continuous loop
while True:
    detect_audio()
    time.sleep(1)  # 1-second pause before next recording
