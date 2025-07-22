"""
EchoFrame Main Entry Point
Author: Alignment Stack
Version: 0.1

A modern offline GUI for running local LLMs using llama.cpp (.gguf models)
"""
import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import EchoFrameWindow

# Ensure models directory exists
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EchoFrameWindow()
    window.show()
    sys.exit(app.exec())
