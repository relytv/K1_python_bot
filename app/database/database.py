from typing import Union
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.database.models import Admin, Group, Location, User


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Комманды супер-админов!
    async def add_admin(self, tg_id: int, username: str, is_superadmin: bool) -> Admin:

        new_admin = Admin(
            tg_id=tg_id,
            username=username,
            is_superadmin=is_superadmin,
        )

        self.session.add(new_admin)
        await self.session.commit()
        return new_admin

    async def get_admin(
        self, tg_id: int | None = None, usernaname: str | None = None
    ) -> Admin | None:
        if tg_id:
            result = await self.session.execute(
                select(Admin).where(Admin.tg_id == tg_id)
            )
        elif usernaname:
            result = await self.session.execute(
                select(Admin).where(Admin.username == usernaname)
            )
        return result.scalar()

    async def is_admin(self, tg_id: int) -> bool:
        result = await self.session.execute(select(Admin.tg_id))
        admin_ids = result.scalars().all()
        return tg_id in admin_ids

    async def is_super_admin(self, tg_id: int) -> bool:
        result = await self.session.execute(
            select(Admin.is_superadmin).where(Admin.tg_id == tg_id)
        )
        result = result.scalar()
        if result:
            return True
        else:
            return False

    async def add_location(self, name: str) -> Location:
        new_location = Location(name=name)
        self.session.add(new_location)
        await self.session.commit()
        return new_location

    async def add_group(
        self, group_name: str, admin_name: str, location_name: str
    ) -> Group:

        admin = await self.get_admin(usernaname=admin_name)
        if not admin:
            raise ValueError(f"Администратор с TG ID {admin_name} не найден")

        location = await self.session.execute(
            select(Location).where(Location.name == location_name)
        )
        location = location.scalar()

        new_group = Group(name=group_name, admin_id=admin.id, location_id=location.id)

        self.session.add(new_group)
        await self.session.commit()
        return new_group

    async def add_user(
        self, username: str, group_name: str, location_name: str, points: int = 0
    ) -> User:

        location = await self.session.execute(
            select(Location).where(Location.name == location_name)
        )
        location = location.scalar()
        print(f"ПРОВЕРКА! {location.id}")

        group = await self.session.execute(
            select(Group).where(
                and_(Group.name == group_name, Group.location_id == location.id)
            )
        )
        group = group.scalar()
        print(f"ПРОВЕРКА! {group}")

        # print(group)

        new_user = User(username=username, group_id=group.id, points=points)

        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_all_group_and_locations(self) -> list[dict]:
        query = select(Group.name, Location.name).join(
            Location, Group.location_id == Location.id
        )

        result = await self.session.execute(query)
        return result.all()

    # Команды тюторов
    async def get_admins_groups(self, tg_id) -> list[dict]:
        admin = await self.get_admin(tg_id=tg_id)

        query = (
            select(Group.name, Location.name, Group.id)
            .join(Group.location)
            .where(Group.admin_id == admin.id)
        )

        result = await self.session.execute(query)
        return result.all()

    async def get_users_by_group_id(self, group_id: uuid.UUID) -> list[User]:
        result = await self.session.execute(
            select(User.username, User.points, User.id).where(User.group_id == group_id)
        )
     
        return result.all()
    
    async def update_user_points(
            self, 
            identifier: Union[uuid.UUID, str], 
            points: int
        ):
        if isinstance(identifier, uuid.UUID):
            user = await self.session.get(User, identifier)
        else:
            user = await self.session.execute(
                select(User).where(User.username == identifier)
            )
            user = user.scalar_one_or_none()

        if user:
            user.points += points
            await self.session.commit()
            return True
        return False
            

    # привязка tg аккаунта пользователя

    async def get_user_by_tg_id(self, tg_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalar_one_or_none()

    async def get_user_by_name(self, name: str) -> User | None:
        result = await self.session.execute(select(User).where(User.username == name))
        return result.scalar_one_or_none()

    async def link_telegram_id(self, user_id: int, tg_id: int):
        user = await self.session.get(User, user_id)
        if user:
            user.tg_id = tg_id
            await self.session.commit()

    # Команды Пользователей

    async def get_cyberons(self, tg_id) -> int:
        user = await self.session.execute(select(User).where(User.tg_id == tg_id))
        result = user.scalar()
        print(f"ПРОВЕРКА {result.points}")

        return result.points
    

    
