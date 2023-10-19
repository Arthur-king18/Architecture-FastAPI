from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import List

from app.presentation.schemas.slide import SlideSchema


class GetPresentationsListResponseSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="ID")
    title: str = Field(..., description="Title")
    subject: str = Field(..., description="Subject")

    class Config:
        orm_mode = True


class CreatePresentationRequestSchema(BaseModel):
    # id: UUID = Field(default_factory=uuid4, description="ID")
    prompt: str = Field(..., description="User prompt")
    title: str = Field(..., description="Title")
    subject: str = Field(..., description="Subject")

    # slides: List[SlideSchema] = Field(..., description="Slides")

    class Config:
        orm_mode = True



class CreatePresentationResponseSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="ID")
    title: str = Field(..., description="Title")
    subject: str = Field(..., description="Subject")

    class Config:
        orm_mode = True
