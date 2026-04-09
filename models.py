from sqlalchemy import Text, BigInteger, Date
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from datetime import date

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int]         = mapped_column(BigInteger, primary_key=True)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str]            = mapped_column(Text, nullable=False)
    created_at: Mapped[date]     = mapped_column(Date, nullable=False)