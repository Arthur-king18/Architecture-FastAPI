from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ImageSchema(BaseModel):
    source: str = Field(default=None, description="Source")
    prompt: str = Field(default=None, description="Prompt")
    resolution: str = Field(default=None, description="Resolution")
    type: str = Field(default=None, description="Type")
    path: str = Field(default=None, description="Path")
    create_at: datetime = Field(default=None, description="Create at")


class SlideSchema(BaseModel):
    title: str = Field(default=None, description="Title")
    bgColor: str = Field(default=None, description="BgColor")
    text: str = Field(default=None, description="Text")
    image: List[ImageSchema] = Field(default=None, description="Image")
    image_background: List[ImageSchema] = Field(default=None, description="Image background")
    image_path: str = Field(default=None, description="Image path")
    image_background_path: str = Field(default=None, description="Image background path")

class SlideResponseSchema(SlideSchema):
    class Config:
        fields = {
            'image': {'exclude': True},
            'image_background': {'exclude': True}
        }


class GetSlidesListResponseSchema(BaseModel):
    slides: List[SlideSchema] = Field(default=None, description="Slides")
    subject: str = Field(default=None, description="Subject")
    title: str = Field(default=None, description="Title")
    prompt: str = Field(default=None, description="Prompt")


class GetPresentationResponseSchema(GetSlidesListResponseSchema):
    slides: List[SlideResponseSchema] = Field(default=None, description="Slides")
