# models.py
import sqlite3
from typing import Protocol

# ─────────────────────────────────────────────────────
# Абстракции (интерфейсы)
# ─────────────────────────────────────────────────────


class DatabaseConnection(Protocol):
    def execute(self, query: str, params: tuple = ()) -> list:
        ...

    def commit(self) -> None:
        ...

    def close(self) -> None:
        ...


# ─────────────────────────────────────────────────────
# Конкретные реализации
# ─────────────────────────────────────────────────────


class Database:
    """Объект конфигурации БД"""

    def __init__(self, dsn: str):
        self.dsn = dsn
        print(f"🗄️  Database object created (dsn={dsn})")


class SQLiteConnection:
    """Реализация соединения с SQLite"""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def execute(self, query: str, params: tuple = ()) -> list:
        cursor = self._conn.execute(query, params)
        return cursor.fetchall()

    def commit(self) -> None:
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


class UserRepository:
    """Репозиторий пользователей"""

    def __init__(self, connection: DatabaseConnection):
        self.connection = connection
        print("👤 UserRepository created")

    def get_user(self, user_id: int) -> dict:
        result = self.connection.execute(
            "SELECT id, name FROM users WHERE id = ?",
            (user_id,)
        )
        if result:
            return {"id": result[0][0], "name": result[0][1]}
        return {"id": user_id, "name": "Alice"}


class UserService:
    """Сервис пользователей"""

    def __init__(self, repo: UserRepository):
        self.repo = repo
        print("⚙️  UserService created")

    def get_profile(self, user_id: int) -> dict:
        user = self.repo.get_user(user_id)
        return {"profile": user}
