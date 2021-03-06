import sqlite3

class ConnectionError(Exception):
    pass

class CredentialsError(Exception):
    pass

class SQLError(Exception):
    pass

# класс для реализации протокола менеджера контекста
class UseDatabase:
    def __init__(self, config: dict) -> None:
        self.configuration = config
        
    def __enter__(self) -> 'cursor':
        try:
            self.conn = sqlite3.connect(self.configuration['db'])        
            self.cursor = self.conn.cursor()
            return self.cursor
        except sqlite3.DatabaseError as err:
            raise ConnectionError(err)        
        except sqlite3.ProgrammingError as err:
            raise CredentialsError(err)

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
        if exc_type is sqlite3.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)

    
