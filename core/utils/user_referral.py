from fastapi import Request
from sqlalchemy import update, values, select
from uuid import UUID

from core.db import Transactional, session
from core.utils import UserCredits
from core.exceptions import UserNotFoundException
from core.config import DOMAIN
from app.presentation.services.constants import REFERRAL_CREDITS
from app.user.models import Referral
from api.constants import USER_V1_API_PREFIX


class UserReferral:
    def __init__(self):
        ...

    async def insert_referral(self, referral_id: UUID) -> None:
        user_id = await self.get_user_id_by_referral_id(referral_id)

        if await self.isExist(user_id):
            await self.add_credits(user_id)

            await self.add_count_referral(referral_id)
        else:
            raise UserNotFoundException

    async def get_referral_link(self, user_id: int) -> str:
        referral_id = await self.get_referral_id_by_user_id_if(user_id)

        if await self.isExist(user_id):
            return f"https://{DOMAIN}{USER_V1_API_PREFIX}?referral_id={referral_id}"
        else:
            raise UserNotFoundException

    @staticmethod
    async def get_user_id_by_referral_id(referral_id: UUID) -> int:
        result = await session.execute(select(Referral.user_id).where(Referral.referral_id == referral_id))
        return result.scalars().first()

    @staticmethod
    async def get_referral_id_by_user_id(user_id: int) -> UUID:
        result = await session.execute(select(Referral.referral_id).where(Referral.user_id == user_id))
        return result.scalars().first()

    @staticmethod
    async def isExist(id) -> bool:
        return id is not None

    @staticmethod
    async def add_credits(user_id: int) -> None:
        await UserCredits().add_credits(user_id, REFERRAL_CREDITS)

    @staticmethod
    @Transactional()
    async def add_count_referral(referral_id: UUID) -> None:
        query = update(Referral).where(Referral.referral_id == referral_id).values(
            count_referral=Referral.count_referral + 1)
        await session.execute(query)
