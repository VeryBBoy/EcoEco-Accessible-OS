import os
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Path to the downloaded model
model_path = os.path.expanduser("~/vosk_models/model-en")

# Load the model
if not os.path.exists(model_path):
    print("Model not found. Download it before proceeding.")
    exit(1)

model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Recording configuration
samplerate = 16000
q = queue.Queue()

def callback(indata, frames, time, status):
    """Callback function to capture audio."""
    if status:
        print(status)
    q.put(bytes(indata))

# Start audio capture
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                        channels=1, callback=callback):
    print("Say something in English (Ctrl+C to exit)...")
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            print(recognizer.Result())
        else:
            print(recognizer.PartialResult())
