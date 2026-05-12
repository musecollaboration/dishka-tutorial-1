# providers/repositories.py
from dishka import Provider, Scope, provide

from models import UserRepository


class RepositoryProvider(Provider):
    """Провайдер для слоя репозиториев"""

    # Упрощённая регистрация: Dishka сама проанализирует __init__
    # и найдёт зависимость DatabaseConnection из DatabaseProvider
    user_repo = provide(UserRepository, scope=Scope.REQUEST)

    # При необходимости можно добавить другие репозитории:
    # product_repo = provide(ProductRepository, scope=Scope.REQUEST)
    # order_repo = provide(OrderRepository, scope=Scope.REQUEST)
