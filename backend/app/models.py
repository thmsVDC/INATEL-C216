from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    correct_country: Mapped[str] = mapped_column(String(120), nullable=False)
    flag_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
