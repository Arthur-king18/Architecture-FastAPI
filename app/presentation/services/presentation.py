from typing import Optional, List
from fastapi import Request

from sqlalchemy import or_, select, and_, desc


from app.user.models import User
from app.presentation.models import Presentation, Slide, PromptHistory, Picture
from app.presentation.services.constants import PRICE_ONE_PRESENTATION
from app.presentation.schemas.presentation import GetPresentationsListResponseSchema
from core.db import Transactional, session
from core.utils.user_credits import UserCredits



class PresentationService:
    def __init__(self):
        ...

    async def get_presentations_by_user_id(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> List[Presentation]:
        query = select(Presentation).filter(Presentation.user_id == user_id)

        query = query.offset(offset)
        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @Transactional()
    async def create_presentation(
        self,
        request: Request,
        presentation_data: dict,
    ) -> None:
        user= request.user
        slides_data = presentation_data["slides"]

        presentation = Presentation(
            title=presentation_data["title"],
            subject=presentation_data["subject"],
            user_id=user.id
        )
        prompt_history = PromptHistory(
            prompt=presentation_data["prompt"],
            presentation_id=presentation.id,
            user_id=user.id
        )

        presentation.prompt.append(prompt_history)
        slide_order = 1

        # Create slides and associate them with the presentation
        for slide_data in slides_data:
            slide = Slide(
                header=slide_data["title"],
                bgColor=slide_data["bgColor"],
                paragraph=slide_data["text"],
                order=slide_order,
                presentation_id=presentation.id
            )
            if slide_data["image"] is not None:
                slide.image_path = slide_data["image"][0]["path"]

                prompt_history_image = PromptHistory(
                    prompt=slide_data["image"][0]["prompt"],
                    presentation_id=presentation.id,
                    user_id=user.id
                )

                image = Picture(
                    source=slide_data["image"][0]["source"],
                    prompt=slide_data["image"][0]["prompt"],
                    resolution=slide_data["image"][0]["resolution"],
                    type=slide_data["image"][0]["type"],
                    path=slide_data["image"][0]["path"],
                    create_at=slide_data["image"][0]["create_at"],
                    user_id=user.id
                )

                presentation.prompt.append(prompt_history_image)
                session.add(image)

            if slide_data["image_background"] is not None:
                slide.image_background_path = slide_data["image_background"][0]["path"]

                prompt_history_image_background = PromptHistory(
                    prompt=slide_data["image_background"][0]["prompt"],
                    presentation_id=presentation.id,
                    user_id=user.id
                )

                image_background = Picture(
                    source=slide_data["image_background"][0]["source"],
                    prompt=slide_data["image_background"][0]["prompt"],
                    resolution=slide_data["image_background"][0]["resolution"],
                    type=slide_data["image_background"][0]["type"],
                    path=slide_data["image_background"][0]["path"],
                    create_at=slide_data["image_background"][0]["create_at"],
                    user_id=user.id
                )

                presentation.prompt.append(prompt_history_image_background)

                session.add(image_background)

            session.add(slide)
            presentation.slides.append(slide)
            slide_order += 1

        session.add(presentation)
        session.add(prompt_history)

        await UserCredits().delete_credits(user.id, PRICE_ONE_PRESENTATION)

    async def get_last_id_presentations_by_user_id(
            self,
            user_id: int
    ):
        query = select(Presentation.id).where(Presentation.user_id == user_id).order_by(desc(Presentation.id)).limit(1)

        result = await session.execute(query)
        return result.scalar()




