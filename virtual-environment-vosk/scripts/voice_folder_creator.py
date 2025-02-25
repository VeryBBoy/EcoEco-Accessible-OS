import os
import queue
import sounddevice as sd
import re
from vosk import Model, KaldiRecognizer

# Ruta al modelo de voz
MODEL_PATH = os.path.expanduser("~/vosk_models/model-es")

# Verificar si el modelo existe
if not os.path.exists(MODEL_PATH):
    print("Error: Modelo de voz no encontrado. Asegúrate de haberlo descargado.")
    exit(1)

# Inicializar Vosk
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Configuración de audio
samplerate = 16000
q = queue.Queue()

def callback(indata, frames, time, status):
    """Captura el audio y lo envía a la cola."""
    if status:
        print(status)
    q.put(bytes(indata))

def create_folder(folder_name):
    """Crea una carpeta con el nombre especificado si no existe."""
    folder_path = os.path.expanduser(f"~/") + folder_name
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"📂 Carpeta creada: {folder_path}")
    except Exception as e:
        print(f"⚠️ Error al crear la carpeta: {e}")

print("🎤 Escuchando... Di 'crear carpeta <nombre_de_la_carpeta>'")

# Iniciar la captura de audio
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                        channels=1, callback=callback):
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(f"📢 Reconociendo: {result}")  # Imprimir lo que reconoce Vosk
            text = result.lower()

            # Buscar la frase "crear carpeta <nombre>"
            match = re.search(r'crear carpeta (\w+)', text)
            if match:
                folder_name = match.group(1)
                create_folder(folder_name)