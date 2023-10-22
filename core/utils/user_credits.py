from fastapi import Request
from sqlalchemy import update, values, select

from core.db import Transactional, session
from core.exceptions import CreditsNotEnoughException
from app.user.models import User


class UserCredits:
    def __init__(self):
        ...

    async def get_balance(self, user_id: int) -> float:
        query = select(User.credits).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalars().first()

    @Transactional()
    async def add_credits(self, user_id: int, credit: float) -> None:
        query = update(User).where(User.id == user_id).values(credits=User.credits + credit)
        await session.execute(query)

    @Transactional()
    async def delete_credits(self, user_id: int, credit: float) -> None:
        if await self.get_balance(user_id) < credit:
            raise CreditsNotEnoughException

        query = update(User).where(User.id == user_id).values(credits=User.credits - credit)
        await session.execute(query)
