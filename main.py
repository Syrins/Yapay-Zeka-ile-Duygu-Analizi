# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from utils.logger import setup_logger

def main():
    logger = setup_logger("app_logger", "app.log")
    logger.info("Uygulama başlatıldı.")

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
