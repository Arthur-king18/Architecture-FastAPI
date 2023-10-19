from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import List, Dict, Tuple


class SlideSchema(BaseModel):
    # id: UUID = Field(default_factory=uuid4, description="ID")
    header: str = Field(..., description="Header")
    subheader: str = Field(..., description="Subheader")
    paragraph: str = Field(..., description="Paragraph")
    # order: int = Field(..., description="Order")
    # is_active: bool  = Field(..., description="Is Active")
    # is_deleted: bool  = Field(..., description="Is Deleted")

    class Config:
        orm_mode = True


class GetSlidesListResponseSchema(BaseModel):
    slides: List[SlideSchema] = Field(..., description="Slides")


class CreateSlideRequestSchema(BaseModel):
    header: str = Field(..., description="Header")
    subheader: str = Field(..., description="Subheader")
    paragraph: str = Field(..., description="Paragraph")
    order: int = Field(..., description="Order")
    is_active: bool  = Field(..., description="Is Active")
    is_deleted: bool  = Field(..., description="Is Deleted")


class CreatePresentationResponseSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="ID")
    header: str = Field(..., description="Header")
    subheader: str = Field(..., description="Subheader")
    paragraph: str = Field(..., description="Paragraph")
    order: int = Field(..., description="Order")
    is_active: bool  = Field(..., description="Is Active")
    is_deleted: bool  = Field(..., description="Is Deleted")

    class Config:
        orm_mode = True

