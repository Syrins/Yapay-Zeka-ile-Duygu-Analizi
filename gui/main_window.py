import sys, json, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QFileDialog, QMessageBox, QTabWidget,
    QSplitter, QAction, QMenuBar, QToolBar, QTextBrowser
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import markdown

from sentiment.analyzer import analyze_sentiment
from sentiment.gpt_analyzer import (
    gpt_sentence_analysis, 
    gpt_general_analysis, 
    gpt_personality_analysis, 
    gpt_character_analysis
)
from gui.settings_window import SettingsWindow
from config.config import API_URL

class AnalysisWorker(QThread):
    analysis_done = pyqtSignal(dict, str, str, str, str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        basic_result = analyze_sentiment(self.text)
        sentence_analysis = gpt_sentence_analysis(self.text)
        general_analysis = gpt_general_analysis(self.text)
        personality_analysis = gpt_personality_analysis(self.text)
        character_analysis = gpt_character_analysis(self.text)
        self.analysis_done.emit(basic_result, sentence_analysis, general_analysis, personality_analysis, character_analysis)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yapay Zeka ile Duygu Analizi")
        self.setGeometry(100, 100, 1200, 800)
        self.settings = self.load_settings()
        self.init_ui()
        self.apply_theme(self.settings.get("theme", "Modern Dark"))

    def load_settings(self):
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "api_url": API_URL,
            "model": "gpt-3.5-turbo",
            "positive_threshold": 0.1,
            "negative_threshold": -0.1,
            "theme": "Modern Dark"
        }

    def save_settings_to_file(self):
        try:
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ayarlar kaydedilemedi: {str(e)}")

    def init_ui(self):
        self.create_menu_bar()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Metni buraya girin veya dosya yükleyin...")
        left_layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()
        self.load_file_button = QPushButton("Dosya Yükle")
        self.load_file_button.clicked.connect(self.load_file)
        button_layout.addWidget(self.load_file_button)

        self.analyze_button = QPushButton("Analizi Başlat")
        self.analyze_button.clicked.connect(self.perform_analysis)
        button_layout.addWidget(self.analyze_button)

        self.clear_button = QPushButton("Temizle")
        self.clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_button)

        self.export_button = QPushButton("Sonuçları Dışa Aktar")
        self.export_button.clicked.connect(self.export_analysis)
        button_layout.addWidget(self.export_button)

        left_layout.addLayout(button_layout)
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)

        # Sağ Panel: Sekmeli Analiz Sonuçları
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # Temel Analiz Sekmesi
        self.basic_tab = QWidget()
        basic_layout = QVBoxLayout()
        self.basic_result_browser = QTextBrowser()
        basic_layout.addWidget(self.basic_result_browser)
        self.basic_tab.setLayout(basic_layout)
        self.tab_widget.addTab(self.basic_tab, "Temel Analiz")

        # Cümle Analizi Sekmesi
        self.sentence_tab = QWidget()
        sentence_layout = QVBoxLayout()
        self.sentence_browser = QTextBrowser()
        sentence_layout.addWidget(self.sentence_browser)
        self.sentence_tab.setLayout(sentence_layout)
        self.tab_widget.addTab(self.sentence_tab, "Cümle Analizi")

        # Genel Analiz Sekmesi
        self.general_tab = QWidget()
        general_layout = QVBoxLayout()
        self.general_browser = QTextBrowser()
        general_layout.addWidget(self.general_browser)
        self.general_tab.setLayout(general_layout)
        self.tab_widget.addTab(self.general_tab, "Genel Analiz")

        # Kişilik Analizi Sekmesi
        self.personality_tab = QWidget()
        personality_layout = QVBoxLayout()
        self.personality_browser = QTextBrowser()
        personality_layout.addWidget(self.personality_browser)
        self.personality_tab.setLayout(personality_layout)
        self.tab_widget.addTab(self.personality_tab, "Kişilik Analizi")

        # Karakter Analizi Sekmesi
        self.character_tab = QWidget()
        character_layout = QVBoxLayout()
        self.character_browser = QTextBrowser()
        character_layout.addWidget(self.character_browser)
        self.character_tab.setLayout(character_layout)
        self.tab_widget.addTab(self.character_tab, "Karakter Analizi")

        right_layout.addWidget(self.tab_widget)
        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 800])
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)

    def create_menu_bar(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        file_menu = menubar.addMenu("Dosya")
        open_action = QAction("Dosya Aç", self)
        open_action.triggered.connect(self.load_file)
        file_menu.addAction(open_action)
        export_action = QAction("Dışa Aktar", self)
        export_action.triggered.connect(self.export_analysis)
        file_menu.addAction(export_action)
        exit_action = QAction("Çıkış", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        settings_menu = menubar.addMenu("Ayarlar")
        settings_action = QAction("Ayarları Düzenle", self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

        help_menu = menubar.addMenu("Yardım")
        about_action = QAction("Hakkında", self)
        about_action.triggered.connect(lambda: QMessageBox.information(self, "Hakkında", "Yapay Zeka ile Duygu Analizi Uygulaması"))
        help_menu.addAction(about_action)

        toolbar = QToolBar("Ana Araç Çubuğu", self)
        self.addToolBar(toolbar)
        toolbar.addAction(open_action)
        toolbar.addAction(settings_action)
        toolbar.addAction(export_action)

    def get_css(self):
        return (
            "<style>"
            "body { font-family: Arial, sans-serif; font-size: 14px; }"
            "li { margin-bottom: 5px; }"
            "h1, h2, h3 { }"
            "</style>"
        )

    def perform_analysis(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Hata", "Lütfen analiz için metin girin veya dosya yükleyin.")
            return

        css = self.get_css()
        self.basic_result_browser.setHtml(css + "<p>Temel analiz yapılıyor, lütfen bekleyiniz...</p>")
        self.sentence_browser.setHtml(css + "<p>Cümle analizi yapılıyor, lütfen bekleyiniz...</p>")
        self.general_browser.setHtml(css + "<p>Genel analiz yapılıyor, lütfen bekleyiniz...</p>")
        self.personality_browser.setHtml(css + "<p>Kişilik analizi yapılıyor, lütfen bekleyiniz...</p>")
        self.character_browser.setHtml(css + "<p>Karakter analizi yapılıyor, lütfen bekleyiniz...</p>")

        self.worker = AnalysisWorker(text)
        self.worker.analysis_done.connect(self.on_analysis_done)
        self.worker.start()

    def on_analysis_done(self, basic_result, sentence_analysis, general_analysis, personality_analysis, character_analysis):
        css = self.get_css()
        basic_output = (
            "### Genel Metin Analizi\n"
            f"- **Polarity:** {basic_result['polarity']:.2f}\n"
            f"- **Subjectivity:** {basic_result['subjectivity']:.2f}\n"
            f"- **Genel Duygu:** {basic_result['sentiment']}\n"
            f"- **Kelime Sayısı:** {basic_result['word_count']}\n"
            f"- **Cümle Sayısı:** {basic_result['sentence_count']}\n"
            f"- **Ortalama Kelime Uzunluğu:** {basic_result['avg_word_length']:.2f}\n"
            f"- **Ortalama Cümle Uzunluğu:** {basic_result['avg_sentence_length']:.2f}\n"
            f"- **Noun Phrases:** {', '.join(basic_result['noun_phrases']) if basic_result['noun_phrases'] else 'Yok'}\n"
        )
        self.basic_result_browser.setHtml(css + markdown.markdown(basic_output, extensions=['extra']))
        self.sentence_browser.setHtml(css + markdown.markdown("## Cümle Analizi\n" + sentence_analysis, extensions=['extra']))
        self.general_browser.setHtml(css + markdown.markdown("## Genel Analizi\n" + general_analysis, extensions=['extra']))
        self.personality_browser.setHtml(css + markdown.markdown("## Kişilik Analizi\n" + personality_analysis, extensions=['extra']))
        self.character_browser.setHtml(css + markdown.markdown("## Karakter Analizi\n" + character_analysis, extensions=['extra']))

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.text_edit.setText(content)
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya okunurken bir hata oluştu: {str(e)}")

    def clear_text(self):
        self.text_edit.clear()
        self.basic_result_browser.clear()
        self.sentence_browser.clear()
        self.general_browser.clear()
        self.personality_browser.clear()
        self.character_browser.clear()

    def export_analysis(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Analiz Sonuçlarını Dışa Aktar", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, "w", encoding="utf-8") as f:
                    basic_text = self.basic_result_browser.toPlainText()
                    sentence_text = self.sentence_browser.toPlainText()
                    general_text = self.general_browser.toPlainText()
                    personality_text = self.personality_browser.toPlainText()
                    character_text = self.character_browser.toPlainText()
                    f.write("==== Temel Analiz ====\n" + basic_text + "\n\n")
                    f.write("==== Cümle Analizi ====\n" + sentence_text + "\n\n")
                    f.write("==== Genel Analizi ====\n" + general_text + "\n\n")
                    f.write("==== Kişilik Analizi ====\n" + personality_text + "\n\n")
                    f.write("==== Karakter Analizi ====\n" + character_text + "\n")
                QMessageBox.information(self, "Dışa Aktarım", "Analiz sonuçları başarıyla kaydedildi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Analiz sonuçları kaydedilemedi: {str(e)}")

    def open_settings(self):
        settings_dialog = SettingsWindow(self, current_settings=self.settings)
        if settings_dialog.exec_():
            self.settings = settings_dialog.get_settings()
            self.save_settings_to_file()
            QMessageBox.information(self, "Ayarlar", "Yeni ayarlar uygulandı.")
            self.apply_theme(self.settings.get("theme", "Modern Dark"))

    def apply_theme(self, theme):
        if theme == "Modern Dark":
            style = (
                "QWidget { background-color: #1E1E2F; color: #ffffff; }"
                "QMenuBar { background-color: #27293D; color: #ffffff; }"
                "QToolBar { background-color: #27293D; color: #ffffff; }"
                "QPushButton { background-color: #3A3F5C; color: #ffffff; }"
                "QTextEdit { background-color: #2B2E44; color: #ffffff; }"
                "QLineEdit { background-color: #2B2E44; color: #ffffff; }"
                "QComboBox { background-color: #2B2E44; color: #ffffff; }"
                "QTextBrowser { background-color: #2B2E44; color: #ffffff; }"
                "QTabWidget::pane { border: 1px solid #27293D; }"
                "QTabBar::tab { background: #27293D; color: #ffffff; padding: 5px; margin: 2px; }"
                "QTabBar::tab:selected { background: #3A3F5C; }"
            )
        elif theme == "Modern Light":
            style = (
                "QWidget { background-color: #ffffff; color: #000000; }"
                "QMenuBar { background-color: #f0f0f0; color: #000000; }"
                "QToolBar { background-color: #f0f0f0; color: #000000; }"
                "QPushButton { background-color: #e0e0e0; color: #000000; }"
                "QTextEdit { background-color: #ffffff; color: #000000; }"
                "QLineEdit { background-color: #ffffff; color: #000000; }"
                "QComboBox { background-color: #ffffff; color: #000000; }"
                "QTextBrowser { background-color: #ffffff; color: #000000; }"
                "QTabWidget::pane { border: 1px solid #f0f0f0; }"
                "QTabBar::tab { background: #f0f0f0; color: #000000; padding: 5px; margin: 2px; }"
                "QTabBar::tab:selected { background: #e0e0e0; }"
            )
        else:
            style = ""
        self.setStyleSheet(style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
