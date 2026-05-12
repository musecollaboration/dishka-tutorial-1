# providers/database.py
import sqlite3
from typing import Iterator
from dishka import Provider, Scope, provide

from models import Database, DatabaseConnection, SQLiteConnection


class DatabaseProvider(Provider):
    """Провайдер для инфраструктуры БД"""

    @provide(scope=Scope.APP)
    def get_dsn(self) -> str:
        """Возвращает строку подключения (из конфига или env)"""
        return "app.db"

    @provide(scope=Scope.APP)
    def get_database(self, dsn: str) -> Database:
        """Создаёт объект конфигурации БД"""
        return Database(dsn)

    @provide(scope=Scope.REQUEST)
    def get_connection(self, dsn: str) -> Iterator[DatabaseConnection]:
        """
        Создаёт соединение с БД и обеспечивает финализацию.
        
        ⚠️ Используем генератор с yield для автоматического закрытия
        ресурса при выходе из скоупа.
        """
        conn = sqlite3.connect(dsn)
        # Создаём тестовую таблицу для демонстрации
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Alice')")
        conn.commit()

        print("🔌 SQLite connection opened")
        try:
            # Оборачиваем в наш интерфейс
            yield SQLiteConnection(conn)
        finally:
            # Гарантированное закрытие при выходе из скоупа
            conn.close()
            print("🔌 SQLite connection closed")
