# main.py
from dishka import make_container

from providers.database import DatabaseProvider
from providers.repositories import RepositoryProvider
from providers.services import ServiceProvider

from models import UserService


def main():
    # 🎯 Создаём контейнер, передавая все провайдеры
    # Порядок не имеет значения — Dishka соберёт единый реестр
    container = make_container(
        DatabaseProvider(),
        RepositoryProvider(),
        ServiceProvider(),
    )

    print("\n=== Первый запрос ===")
    with container() as request_container:
        # Запрашиваем сервис — контейнер автоматически построит граф:
        # UserService → UserRepository → DatabaseConnection → dsn
        user_service: UserService = request_container.get(UserService)
        print(f"📋 Profile: {user_service.get_profile(1)}")

    print("\n=== Второй запрос ===")
    with container() as request_container:
        # Получаем НОВЫЙ экземпляр сервиса (скоуп REQUEST)
        user_service2: UserService = request_container.get(UserService)
        print(f"📋 Profile: {user_service2.get_profile(2)}")

    # 🧹 Закрываем контейнер — финализируются APP-зависимости
    container.close()
    print("\n✅ Контейнер закрыт")


if __name__ == "__main__":
    main()
