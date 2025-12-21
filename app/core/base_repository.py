from sqlalchemy.ext.asyncio import AsyncSession

class SqlBaseRepository:
    """Base class for SQL repositories."""

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session=session