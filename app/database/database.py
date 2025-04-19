from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import Admin


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_admin(
        self, 
        tg_id: int, 
        username: str, 
        is_superadmin: bool
    ) -> Admin: 
        
        new_admin = Admin(
            tg_id=tg_id,
            username=username,
            is_superadmin=is_superadmin,
        )
    
        self.session.add(new_admin)
        await self.session.commit()
        return new_admin

    async def get_admin(self, tg_id: int) -> Admin | None:
        result = await self.session.execute(
            select(Admin).where(Admin.tg_id == tg_id)
        )
        return result.scalar()
    

    async def is_admin(self, tg_id: int) -> bool:
        result = await self.session.execute(
            select(Admin.tg_id)
        )
        admin_ids = result.scalars().all()
        return tg_id in admin_ids