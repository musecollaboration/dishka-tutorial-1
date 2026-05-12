# Учебный проект по внедрению зависимостей с Dishka

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Dishka](https://img.shields.io/badge/Dishka-1.10.1-green.svg)](https://github.com/reagento/dishka)

Этот учебный проект демонстрирует использование библиотеки **Dishka** для внедрения зависимостей (Dependency Injection) в приложениях на Python.

## Структура проекта

```
dishka-tutorial-1/
├── main.py               # Демонстрация работы DI контейнера
├── models.py             # Модели данных и интерфейсы
├── providers/            # Провайдеры Dishka для каждого слоя
│   ├── database.py       # Провайдер базы данных
│   ├── repositories.py   # Провайдер репозиториев
│   └── services.py       # Провайдер сервисов
├── pyproject.toml        # Конфигурация проекта (Poetry)
└── README.md
```

## Быстрый старт

### 1. Установка зависимостей

```bash
# Клонирование репозитория (если применимо)
git clone <repository-url>
cd dishka-tutorial-1

# Создание и активация виртуального окружения
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate  # Windows

# Установка зависимостей через Poetry
poetry install

# Или через pip (создать requirements.txt из pyproject.toml)
pip install -r requirements.txt
```

### 2. Запуск демонстрации

```bash
python main.py
```

## Что демонстрирует проект

### Основные концепции:

1. **Внедрение зависимостей**: Автоматическое создание и управление зависимостями
2. **Скоупы жизненного цикла**:
   - `APP` - синглтоны (конфигурация БД)
   - `REQUEST` - объекты на каждый запрос (соединения, сервисы)
3. **Архитектура**: Разделение на слои Infrastructure, Repository, Service
4. **Автоматическое разрешение**: Dishka самостоятельно строит граф зависимостей

### Пример работы:

```python
# Создание контейнера с провайдерами
container = make_container(
    DatabaseProvider(),
    RepositoryProvider(),
    ServiceProvider(),
)

# Использование в запросе
with container() as request_container:
    user_service = request_container.get(UserService)
    profile = user_service.get_profile(1)
```

## Архитектурные слои

### 1. Infrastructure Layer (`providers/database.py`)

- Управляет подключением к базе данных
- Создает и конфигурирует соединения
- Обеспечивает правильное закрытие ресурсов

### 2. Repository Layer (`models.py` + `providers/repositories.py`)

- Предоставляет доступ к данным
- Инкапсулирует логику работы с БД
- Работает через интерфейсы абстракций

### 3. Service Layer (`models.py` + `providers/services.py`)

- Содержит бизнес-логику
- Использует репозитории для доступа к данным
- Не зависит от конкретной реализации БД

## Технологический стек

### Основные зависимости:

- **Dishka** 1.10.1 - Внедрение зависимостей

## Изучаемые концепции

### Внедрение зависимостей:

- **Provider pattern**: Регистрация зависимостей
- **Scope management**: Управление жизненным циклом объектов
- **Dependency graph resolution**: Автоматическое разрешение зависимостей
- **Protocol-based interfaces**: Абстракции через типы

### Архитектура:

- **Separation of concerns**: Разделение ответственности
- **Dependency inversion**: Зависимость от абстракций, а не от конкретики
- **Layered architecture**: Четкое разделение слоев

## Примеры кода

### Создание провайдера:

```python
from dishka import Provider, Scope, provide

class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_dsn(self) -> str:
        return "app.db"

    @provide(scope=Scope.REQUEST)
    def get_connection(self, dsn: str) -> DatabaseConnection:
        # Создание соединения с БД
        return SQLiteConnection(sqlite3.connect(dsn))
```

### Определение зависимостей:

```python
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_profile(self, user_id: int) -> dict:
        return self.repo.get_user(user_id)
```

## Тестирование

Проект готов для тестирования:

```bash
# Установка тестовых зависимостей
pip install pytest pytest-asyncio

# Запуск тестов
pytest
```

## Расширение проекта

### Добавление нового компонента:

1. **Определите интерфейс** в `models.py`:

```python
class ProductRepository(Protocol):
    def get_product(self, product_id: int) -> dict: ...
```

2. **Создайте реализацию** в `models.py`:

```python
class ProductRepository:
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def get_product(self, product_id: int) -> dict:
        # Логика получения продукта
        pass
```

3. **Добавьте провайдер** в `providers/repositories.py`:

```python
class RepositoryProvider(Provider):
    product_repo = provide(ProductRepository, scope=Scope.REQUEST)
```

4. **Используйте в сервисе**:

```python
class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo
```

## Полезные ресурсы

- [Официальная документация Dishka](https://dishka.readthedocs.io/en/stable/quickstart.html)

## Вклад в проект

Если вы хотите внести вклад в этот учебный проект:

1. Форкните репозиторий
2. Создайте ветку для вашей feature
3. Внесите изменения
4. Создайте Pull Request

## Лицензия

Этот учебный проект распространяется под лицензией MIT.

---

**Создано для демонстрации принципов Dependency Injection**
