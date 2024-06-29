import factory
import factory.fuzzy

from mader.models import User
from mader.utils import sanitizar_username


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: sanitizar_username(f'test{n}'))
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    senha = factory.LazyAttribute(lambda obj: f'{obj}.username@test.com')
