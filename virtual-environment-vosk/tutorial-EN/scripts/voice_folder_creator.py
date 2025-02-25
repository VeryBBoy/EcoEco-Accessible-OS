import os
import queue
import sounddevice as sd
import re
from vosk import Model, KaldiRecognizer

# Path to the voice model
MODEL_PATH = os.path.expanduser("~/vosk_models/model-en")

# Verify if the model exists
if not os.path.exists(MODEL_PATH):
    print("Error: Voice model not found. Make sure you have downloaded it.")
    exit(1)

# Initialize Vosk
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Audio configuration
samplerate = 16000
q = queue.Queue()

def callback(indata, frames, time, status):
    """Captures audio and sends it to the queue."""
    if status:
        print(status)
    q.put(bytes(indata))

def create_folder(folder_name):
    """Creates a folder with the specified name if it does not exist."""
    folder_path = os.path.expanduser(f"~/") + folder_name
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"📂 Folder created: {folder_path}")
    except Exception as e:
        print(f"⚠️ Error creating folder: {e}")

print("🎤 Listening... Say 'create folder <folder_name>'")

# Start audio capture
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                        channels=1, callback=callback):
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(f"📢 Recognizing: {result}")  # Print what Vosk recognizes
            text = result.lower()

            # Search for the phrase "create folder <name>"
            match = re.search(r'create folder (\w+)', text)
            if match:
                folder_name = match.group(1)
                create_folder(folder_name)
