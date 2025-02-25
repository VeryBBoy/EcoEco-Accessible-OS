import os
import sys
import queue
import json
import threading
import re
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox

# Path to the English voice model
MODEL_PATH = os.path.expanduser("~/vosk_models/model-en")

# Audio queue for real-time processing
audio_queue = queue.Queue()

class VoiceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Voice Recognition with Vosk")
        self.setGeometry(100, 100, 400, 200)

        # Label to display recognized text
        self.label = QLabel("Listening...", self)
        
        # Exit button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close)

        # Interface layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.exit_button)
        self.setLayout(layout)

        # Start voice recognition in a separate thread
        self.running = True
        self.recognition_thread = threading.Thread(target=self.recognize_speech)
        self.recognition_thread.start()

    def recognize_speech(self):
        """ Captures and processes audio with Vosk """
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
                        print(f"Recognized: {text}")
                        self.label.setText(f"Recognized: {text}")
                        self.process_command(text)

    def process_command(self, text):
        """ Processes voice commands """
        match = re.search(r"create folder (.+)", text)
        if match:
            folder_name = match.group(1).strip()
            os.makedirs(folder_name, exist_ok=True)
            self.show_message(f"Folder '{folder_name}' created successfully.")

    def show_message(self, message):
        """ Displays a message in a pop-up window """
        msg = QMessageBox(self)
        msg.setWindowTitle("Notification")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def closeEvent(self, event):
        """ Handles application closure """
        self.running = False
        self.recognition_thread.join()
        event.accept()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceRecognitionApp()
    window.show()
    sys.exit(app.exec())
