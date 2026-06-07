from src.repo.refresh_token import RefreshTokenRepository
from src.repo.roles import RolesRepository, UserRolesRepository
from src.repo.users import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.refresh_token = RefreshTokenRepository(self.session)
        self.roles = RolesRepository(self.session)
        self.user_roles = UserRolesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()