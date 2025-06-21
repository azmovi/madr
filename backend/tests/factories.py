import factory

from mader.models import Role, User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Faker('name')
    email = factory.Faker('email')
    senha = factory.Faker('password')
    role = Role.USER


class AdminFactory(UserFactory):
    role = Role.ADMIN
