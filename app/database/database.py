from sqlalchemy.ext.asyncio import AsyncSession


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session
