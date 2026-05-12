# providers/services.py
from dishka import Provider, Scope, provide

from models import UserService


class ServiceProvider(Provider):
    """Провайдер для слоя сервисов"""

    # Dishka автоматически найдёт UserRepository из RepositoryProvider
    user_service = provide(UserService, scope=Scope.REQUEST)
