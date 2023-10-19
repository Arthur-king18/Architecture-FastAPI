from pydantic import BaseModel
from typing import List


class ValidSlideSchema(BaseModel):
    title: str
    bgColor: str
    text: str

class ValidSlidesListResponseSchema(BaseModel):
    subject: str
    title: str
    slides: List[ValidSlideSchema]