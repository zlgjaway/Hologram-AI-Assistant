import pyaudio
import wave
import whisper

import os
from gtts import gTTS
import playsound
import pyjokes
# Set up parameters for recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5


# Initialize PyAudio
audio = pyaudio.PyAudio()

# Function to capture audio from the microphone
def capture_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Listening...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    wave_output_filename = "output.wav"
    waveFile = wave.open(wave_output_filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    return wave_output_filename

# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result['text']


# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    playsound.playsound("response.mp3")

def joke():
    funny = pyjokes.get_joke()
    print(funny)
    playsound.playsound("Here is your favorite joke: " + funny)

# Main loop
command = ""

while True:
        try:
            command = capture_audio()
            if "joke" in command:
               joke()
        except Exception as e:
            print(f"Oops, there was an error: {e}")     
                 
             