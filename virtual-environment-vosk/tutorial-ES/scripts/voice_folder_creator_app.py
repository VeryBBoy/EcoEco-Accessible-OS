import os
import sys
import queue
import json
import threading
import re
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox

# Ruta del modelo de voz en español
MODEL_PATH = os.path.expanduser("~/vosk_models/model-es")

# Cola de audio para procesamiento en tiempo real
audio_queue = queue.Queue()

class VoiceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reconocimiento de Voz con Vosk")
        self.setGeometry(100, 100, 400, 200)

        # Etiqueta para mostrar el texto reconocido
        self.label = QLabel("Escuchando...", self)
        
        # Botón para salir
        self.exit_button = QPushButton("Salir", self)
        self.exit_button.clicked.connect(self.close)

        # Diseño de la interfaz
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.exit_button)
        self.setLayout(layout)

        # Iniciar el reconocimiento de voz en un hilo separado
        self.running = True
        self.recognition_thread = threading.Thread(target=self.recognize_speech)
        self.recognition_thread.start()

    def recognize_speech(self):
        """ Captura y procesa el audio con Vosk """
        model = Model(MODEL_PATH)
        recognizer = KaldiRecognizer(model, 16000)

        def callback(indata, frames, time, status):
            if status:
                print(status)
            audio_queue.put(bytes(indata))

        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                               channels=1, callback=callback):
            while self.running:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").lower()
                    if text:
                        print(f"Reconocido: {text}")
                        self.label.setText(f"Reconocido: {text}")
                        self.process_command(text)

    def process_command(self, text):
        """ Procesa los comandos de voz """
        match = re.search(r"crear carpeta (.+)", text)
        if match:
            folder_name = match.group(1).strip()
            os.makedirs(folder_name, exist_ok=True)
            self.show_message(f"Carpeta '{folder_name}' creada correctamente.")

    def show_message(self, message):
        """ Muestra un mensaje en una ventana emergente """
        msg = QMessageBox(self)
        msg.setWindowTitle("Notificación")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def closeEvent(self, event):
        """ Maneja el cierre de la aplicación """
        self.running = False
        self.recognition_thread.join()
        event.accept()

# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceRecognitionApp()
    window.show()
    sys.exit(app.exec())

