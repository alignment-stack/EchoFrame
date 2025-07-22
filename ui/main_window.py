"""
EchoFrame Main Window UI
Author: Alignment Stack
"""
from llama_cpp import Llama
import markdown
from rich.markdown import Markdown
from rich.console import Console
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QScrollArea, QFrame, QComboBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import scan_models_folder

class EchoFrameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing EchoFrameWindow...")
        self.selected_model = None
        self.model_metadata = {}
        self.token_count = 0
        self.ram_usage = 0.0
        self.llama_model = None  # Ensure llama_model is always defined
        self.chat_area = QTextEdit()  # Ensure chat_area is always defined
        self.setWindowTitle("EchoFrame")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("""
            * { font-family: 'Roboto Condensed', 'Segoe UI', Arial, sans-serif; }
            background-color: #181A20; color: #E0E0E0;
        """)
        print("Calling init_ui...")
        self.init_ui()
        print("UI initialization complete.")
    def load_selected_model(self):
        """Stub for loading the selected model. Fill in with actual model loading logic."""
        # Example: Load the model using llama_cpp or your own logic
        # if self.selected_model:
        #     model_path = os.path.join(os.path.dirname(__file__), '..', 'models', self.selected_model)
        #     self.llama_model = Llama(model_path)
        #     # Optionally update model info box, etc.
        pass

    def show_model_info(self):
        """Stub for displaying model information. Fill in with actual info display logic."""
        # Example: Update a model info box or display metadata
        # if self.selected_model:
        #     info = self.model_metadata.get(self.selected_model, {})
        #     # Update info box widget, etc.
        pass

    def init_ui(self):
        print("Setting up UI components...")
        # Header
        header = QFrame()
        header.setStyleSheet("background: #181A20; border-bottom: 1px solid #00FFF7;")
        header_layout = QVBoxLayout()
        logo = QLabel("EchoFrame")
        logo.setFont(QFont("Segoe UI", 24, QFont.Bold))
        logo.setStyleSheet("color: #00FFF7; text-shadow: 0 0 8px #00FFF7;")
        subtext = QLabel("by Alignment Stack")
        subtext.setFont(QFont("Segoe UI", 10))
        subtext.setStyleSheet("color: #A0A0A0;")
        header_layout.addWidget(logo)
        header_layout.addWidget(subtext)
        header.setLayout(header_layout)
        self.header = header
        print("Header setup complete.")

        # Model selection dropdown
        model_box = QFrame()
        model_box.setStyleSheet("background: #20232A; border: 1px solid #00FFF7; border-radius: 8px; margin-bottom: 12px;")
        model_layout = QVBoxLayout(model_box)
        model_label = QLabel("Model")
        model_label.setStyleSheet("color: #00FFF7; font-weight: bold; margin-bottom: 4px;")
        self.model_dropdown = QComboBox()
        self.model_dropdown.setStyleSheet("background: #20232A; color: #E0E0E0; border-radius: 6px; padding: 8px;")
        self.model_dropdown.currentIndexChanged.connect(self.select_model)
        self.load_models_dropdown()
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_dropdown)
        self.model_box = model_box
        print("Model selection dropdown setup complete.")

        # Chat area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont("Roboto Condensed", 12))
        self.chat_area.setStyleSheet(
            "background: #181A20; color: #E0E0E0; "
            "border: 2px solid #00FFF7; "
            "border-radius: 10px; "
            "padding: 8px; "
            "font-family: 'Roboto Condensed', 'Segoe UI', sans-serif;"
        )
        print("Chat area setup complete.")

        # --- Refined UI Layout ---
        # Settings panel (sidebar)
        settings_box = QFrame()
        settings_box.setStyleSheet("background: #23242A; border: 1px solid #00FFF7; border-radius: 12px; padding: 16px; margin: 0 0 0 12px;")
        settings_layout = QVBoxLayout()
        settings_header = QLabel("Model Settings")
        settings_header.setStyleSheet("color: #00FFF7; font-size: 18px; font-weight: bold; margin-bottom: 16px;")
        settings_layout.addWidget(settings_header)

        # Add a divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("border: none; background: #00FFF7; min-height: 2px; margin-bottom: 12px;")
        settings_layout.addWidget(divider)

        # Max Tokens
        max_tokens_label = QLabel("Max Tokens")
        max_tokens_label.setStyleSheet("color: #00FFF7; font-size: 14px; margin-bottom: 2px;")
        self.max_tokens_input = QLineEdit()
        self.max_tokens_input.setPlaceholderText("256")
        self.max_tokens_input.setStyleSheet("background: #23242A; color: #E0E0E0; border-radius: 6px; padding: 6px; margin-bottom: 10px;")
        settings_layout.addWidget(max_tokens_label)
        settings_layout.addWidget(self.max_tokens_input)

        # Temperature
        temperature_label = QLabel("Temperature")
        temperature_label.setStyleSheet("color: #00FFF7; font-size: 14px; margin-bottom: 2px;")
        self.temperature_input = QLineEdit()
        self.temperature_input.setPlaceholderText("0.7")
        self.temperature_input.setStyleSheet("background: #23242A; color: #E0E0E0; border-radius: 6px; padding: 6px; margin-bottom: 10px;")
        settings_layout.addWidget(temperature_label)
        settings_layout.addWidget(self.temperature_input)

        # Top-k Sampling
        top_k_label = QLabel("Top-k Sampling")
        top_k_label.setStyleSheet("color: #00FFF7; font-size: 14px; margin-bottom: 2px;")
        self.top_k_input = QLineEdit()
        self.top_k_input.setPlaceholderText("40")
        self.top_k_input.setStyleSheet("background: #23242A; color: #E0E0E0; border-radius: 6px; padding: 6px; margin-bottom: 10px;")
        settings_layout.addWidget(top_k_label)
        settings_layout.addWidget(self.top_k_input)

        # Top-p Sampling
        top_p_label = QLabel("Top-p Sampling")
        top_p_label.setStyleSheet("color: #00FFF7; font-size: 14px; margin-bottom: 2px;")
        self.top_p_input = QLineEdit()
        self.top_p_input.setPlaceholderText("0.9")
        self.top_p_input.setStyleSheet("background: #23242A; color: #E0E0E0; border-radius: 6px; padding: 6px; margin-bottom: 10px;")
        settings_layout.addWidget(top_p_label)
        settings_layout.addWidget(self.top_p_input)

        settings_box.setLayout(settings_layout)

        # Main content area (chat, prompt, info)
        content_box = QFrame()
        content_box.setStyleSheet("background: #181A20; border-radius: 12px; padding: 16px;")
        content_layout = QVBoxLayout()
        content_layout.setSpacing(16)
        content_layout.addWidget(self.header)
        content_layout.addWidget(self.model_box)

        # Info box
        self.info_box = QFrame()
        self.info_box.setStyleSheet("background: #20232A; border: 1px solid #00FFF7; border-radius: 8px; padding: 8px;")
        info_layout = QVBoxLayout(self.info_box)
        self.token_label = QLabel("Tokens: 0")
        self.token_label.setStyleSheet("color: #00FFF7; font-size: 14px;")
        self.ram_label = QLabel("RAM: N/A")
        self.ram_label.setStyleSheet("color: #00FFF7; font-size: 14px;")
        info_layout.addWidget(self.token_label)
        info_layout.addWidget(self.ram_label)
        self.info_box.setLayout(info_layout)

        content_layout.addWidget(self.info_box)
        content_layout.addWidget(self.chat_area)
        # Prompt box
        self.prompt_box = QHBoxLayout()
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Type your message here...")
        self.prompt_input.setStyleSheet("background: #23242A; color: #E0E0E0; border-radius: 6px; padding: 6px;")
        send_button = QPushButton("Send")
        send_button.setStyleSheet("background: #00FFF7; color: #181A20; border-radius: 6px; padding: 6px;")
        send_button.clicked.connect(self.handle_send)
        self.prompt_box.addWidget(self.prompt_input)
        self.prompt_box.addWidget(send_button)

        content_layout.addLayout(self.prompt_box)
        content_box.setLayout(content_layout)

        # Two-column layout: main content and settings sidebar
        main_layout = QHBoxLayout()
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.addWidget(content_box, 3)
        main_layout.addWidget(settings_box, 1)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_models_dropdown(self):
        """Populate the model dropdown with available models."""
        models = scan_models_folder(os.path.join(os.getcwd(), "models"))
        self.model_dropdown.clear()
        self.model_dropdown.addItems(models)

    def select_model(self, index):
        """Handle model selection from dropdown."""
        if index < 0:
            return
        self.selected_model = self.model_dropdown.itemText(index)
        self.chat_area.append(f"<span style='color:#00FFF7'><b>Selected model:</b> {self.selected_model}</span>")
        self.load_selected_model()
        if self.llama_model:
            self.chat_area.append("<span style='color:green'><b>Model loaded successfully.</b></span>")
        else:
            self.chat_area.append("<span style='color:red'><b>Model failed to load.</b></span>")
        self.show_model_info()

    def load_models_dropdown(self):
        """Populate the model dropdown with available models."""
        models = scan_models_folder(os.path.join(os.getcwd(), "models"))
        self.model_dropdown.clear()
        self.model_dropdown.addItems(models)

    def handle_send(self):
        """Handle sending a prompt and displaying the response."""
        prompt = self.prompt_input.text().strip()
        if not prompt:
            return
        self.chat_area.append(f"<b>You:</b> {prompt}")
        self.prompt_input.clear()
        response = self.get_model_response(prompt)
        self.chat_area.append(f"<b>EchoFrame:</b> {response}")
        self.token_count = len(prompt.split()) + len(response.split())
        self.token_label.setText(f"Tokens: {self.token_count}")
        try:
            import psutil
            ram_gb = psutil.virtual_memory().used / (1024 ** 3)
            self.ram_label.setText(f"RAM: {ram_gb:.2f} GB")
        except ImportError:
            self.ram_label.setText("RAM: N/A")

    def get_model_response(self, prompt):
        """Generate a response from the loaded model."""
        if self.llama_model is not None:
            try:
                if hasattr(self.llama_model, 'create_completion'):
                    output = self.llama_model.create_completion(prompt, max_tokens=256)
                    return output['choices'][0]['text'].strip()
                else:
                    output = self.llama_model(prompt, max_tokens=256)
                    return output['choices'][0]['text'].strip()
            except Exception as e:
                return f"<span style='color:red'><b>Model error:</b> {e}</span>"
        else:
            return "<span style='color:red'><b>No model loaded. Please select a model and ensure it loads successfully.</b></span>"

