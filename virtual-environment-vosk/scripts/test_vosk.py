import os
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Ruta al modelo descargado
model_path = os.path.expanduser("~/vosk_models/model-es")

# Cargar el modelo
if not os.path.exists(model_path):
    print("Modelo no encontrado. Descárgalo antes de continuar.")
    exit(1)

model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Configuración de grabación
samplerate = 16000
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                        channels=1, callback=callback):
    print("Di algo (Ctrl+C para salir)...")
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            print(recognizer.Result())
        else:
            print(recognizer.PartialResult())