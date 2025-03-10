# gui/settings_window.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QDoubleSpinBox, QPushButton, QMessageBox
from config.config import API_KEYS, API_URL

class SettingsWindow(QDialog):
    def __init__(self, parent=None, current_settings=None):
        super().__init__(parent)
        self.setWindowTitle("Ayarlar")
        self.resize(400, 300)
        self.current_settings = current_settings if current_settings is not None else {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # API URL ayarı
        self.api_url_edit = QLineEdit()
        self.api_url_edit.setText(self.current_settings.get("api_url", API_URL))
        form_layout.addRow("API URL:", self.api_url_edit)

        # API Anahtarları
        self.api_keys_edit = QLineEdit()
        self.api_keys_edit.setText(", ".join(API_KEYS))
        self.api_keys_edit.setReadOnly(True)
        form_layout.addRow("API Anahtarları:", self.api_keys_edit)

        # Model seçimi
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-3.5-turbo", "gpt-4"])
        self.model_combo.setCurrentText(self.current_settings.get("model", "gpt-3.5-turbo"))
        form_layout.addRow("Model Seçimi:", self.model_combo)

        # Olumlu duygu eşiği
        self.positive_threshold_spin = QDoubleSpinBox()
        self.positive_threshold_spin.setDecimals(2)
        self.positive_threshold_spin.setRange(0.0, 1.0)
        self.positive_threshold_spin.setSingleStep(0.05)
        self.positive_threshold_spin.setValue(self.current_settings.get("positive_threshold", 0.1))
        form_layout.addRow("Olumlu Eşiği:", self.positive_threshold_spin)

        # Olumsuz duygu eşiği
        self.negative_threshold_spin = QDoubleSpinBox()
        self.negative_threshold_spin.setDecimals(2)
        self.negative_threshold_spin.setRange(-1.0, 0.0)
        self.negative_threshold_spin.setSingleStep(0.05)
        self.negative_threshold_spin.setValue(self.current_settings.get("negative_threshold", -0.1))
        form_layout.addRow("Olumsuz Eşiği:", self.negative_threshold_spin)

        # Tema seçimi
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setCurrentText(self.current_settings.get("theme", "Light"))
        form_layout.addRow("Tema Seçimi:", self.theme_combo)

        layout.addLayout(form_layout)

        self.save_button = QPushButton("Ayarları Kaydet")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_settings(self):
        self.current_settings["api_url"] = self.api_url_edit.text().strip()
        self.current_settings["model"] = self.model_combo.currentText()
        self.current_settings["positive_threshold"] = self.positive_threshold_spin.value()
        self.current_settings["negative_threshold"] = self.negative_threshold_spin.value()
        self.current_settings["theme"] = self.theme_combo.currentText()

        QMessageBox.information(self, "Ayarlar", "Ayarlar kaydedildi!")
        self.accept()

    def get_settings(self):
        return self.current_settings
