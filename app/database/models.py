import uuid
from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey


class Admin(Base):
    __tablename__ = "admins"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tg_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    username: Mapped[str]
    is_superadmin: Mapped[bool] = mapped_column(default=False)
    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id", ondelete="SET NULL")
    )


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(default=0)
    points: Mapped[int]
    group_id = Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id")
    )
    group = relationship("Group", back_populates="users")


class Location(Base):
    __tablename__ = "groups"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(nullable=False)
    groups = relationship("Group", back_populates="location")


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[uuid.UUID] = mapped_column(String, nullable=False)

    location_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("locations.id")
    )  # Связь с локацией
    admin_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admins.id")
    )  # Связь с админом (один админ в группе)

    location = relationship("Location", back_populates="groups")  # Связь с локацией
    admin = relationship("Admin", back_populates="group")  # Связь с админом
    users = relationship("User", back_populates="group")  # Связь с пользователями
