# SilentSense-# 🎤 Speech-to-Text on ESP32 OLED

This project captures your **voice on a PC**, converts it into text using Python’s SpeechRecognition library, and then sends the text to an **ESP32 microcontroller**, which displays it on an **I2C OLED screen (SSD1306)**.

---

## 🚀 Features
- Speech-to-Text conversion using Google Speech Recognition API  
- Sends text to ESP32 over Wi-Fi (HTTP request)  
- ESP32 hosts a mini web server to receive text  
- Displays text on SSD1306 OLED in real-time  

---

## 🖥️ Python Client (PC Side)
### Requirements
Install dependencies:
```bash
pip install -r requirements.txt
