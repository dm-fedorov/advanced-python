import sqlite3

# класс для реализации протокола менеджера контекста
class UseDatabase:
    def __init__(self, config: dict) -> None:
        self.configuration = config
        
    def __enter__(self) -> 'cursor':        
        self.conn = sqlite3.connect(self.configuration['db'])        
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    
