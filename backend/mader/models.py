from datetime import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry, validates

from mader.schemas import Role
from mader.utils import criptografar_senha, sanitizar_username

table_registry = registry()


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class User(TimestampMixin):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=func.gen_random_uuid()
    )
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    role: Mapped[Role]

    @validates('username')
    def validate_username(self, key, username):  # noqa: PLR6301
        try:
            return sanitizar_username(username)
        except Exception:
            raise ValueError(f'Fail to sanitize the username: {username}')

    @validates('senha')
    def hash_senha(self, key, senha):  # noqa: PLR6301
        try:
            return criptografar_senha(senha)
        except Exception:
            raise ValueError('Fail to cryptography the senha')
