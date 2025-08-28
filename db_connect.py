import logging
import psycopg2
import os
from datetime import datetime
from logging_config import set_logs

# для логгов
logger = set_logs(datetime.now())
    
class DatabaseConnection:
    _instance = None

    def __new__(cls, *args):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        else: 
            logging.warning(f'Повторное создание экземпляра класса для подключения к базе данных')
        return cls._instance
        
    def __init__(self, database, user, password, host, port):
        try:
            if not hasattr(self, 'instance'):  # Проверяем, существует ли экземпляр
                self.__database = database
                self.__user = user
                self.__password = password
                self.__host = host
                self.__port = port
        except Exception as e:
            logging.error(f'Ошибка подключения к базе данных: {e}')

    
    def __enter__(self):
        try:
            self.connection = psycopg2.connect(database=self.__database, 
                                                    user=self.__user, 
                                                password=self.__password,
                                                    host=self.__host, 
                                                    port=self.__port)
            self.cursor = self.connection.cursor()
            self.status = True
            logging.info(f'Подключение к базе данных успешно установлено')
        except Exception as e:
            self.status = False
            logging.error(f'Ошибка подключения к базе данных: {e}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): # закрытие соединения
        self.cursor.close()
        self.connection.close()
        logging.info(f'Соединение с базой данных закрыто')    

    def try_query(self, query, params=None): # обычные запросы + параметризированные запросы
        try: 
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            logging.info(f'Запрос выполнен успешно')    
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f'Ошибка при выполнении запроса: {e}')
            self.connection.rollback()

    def insert_data(self, insert_query, data, file_name): # для вставки данных отдельный метод
        try:
            self.cursor.executemany(insert_query, data)
            self.connection.commit()
            logging.info(f'Файл {file_name} перенесен в базу данных')
            # в случае успеха файл удаляется
            os.remove(file_name)
        except Exception as e:
            logging.error(f'Ошибка при вставке данных из файла {file_name}; {e}')
            # в случае ошибки файл переименовывается
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            name, extension = os.path.splitext(filename)
            # Создаем новое имя файла
            new_filename = f"error_{datetime.now().date().strftime('%Y-%m-%d')}_{name}{extension}"
            new_path = os.path.join(directory, new_filename)
            os.rename(file_name,  new_path)
            self.connection.rollback()