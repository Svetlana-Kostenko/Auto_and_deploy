import logging
from datetime import datetime


def set_logs(current_date):
        log_filename = f'app_{current_date.strftime('%Y-%m-%d')}.log'
        #Настройка логирования в файл
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=log_filename,
            filemode='a',
            encoding='cp1251'
        )

        # Получаем текущий логгер
        logger = logging.getLogger()
        
        # Находим FileHandler в обработчиках
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                return handler
                