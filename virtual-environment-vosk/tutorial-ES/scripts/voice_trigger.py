import queue
import sounddevice as sd
import json
import vosk
import subprocess

# Configurar el modelo de Vosk
MODEL_PATH = os.path.expanduser("~/vosk_models/model-es")
SAMPLE_RATE = 16000  # Frecuencia de muestreo
TRIGGER_WORDS = ["eco eco"]  # Palabras clave para activar la app
APP_PATH = "python voice_folder_creator_app.py"  # Ruta de la app a ejecutar

# Cola para procesar el audio
q = queue.Queue()

# Función de callback para capturar audio en tiempo real
def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

# Inicializar el reconocedor
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

# Iniciar la captura de audio
with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype="int16",
                       channels=1, callback=callback):
    print("🎤 Escuchando... Di 'eco eco' para ejecutar la aplicación.")

    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower()
            print(f"🗣️ Reconocido: {text}")

            if any(trigger in text for trigger in TRIGGER_WORDS):
                print("✅ Activando aplicación...")
                subprocess.run(APP_PATH, shell=True)
