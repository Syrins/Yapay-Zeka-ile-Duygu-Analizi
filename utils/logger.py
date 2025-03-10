# utils/logger.py

import logging

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    # encoding parametresini ekleyerek utf-8 olarak ayarlıyoruz
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger

# Örnek kullanım:
# logger = setup_logger("app_logger", "app.log")
# logger.info("Uygulama başlatıldı")
