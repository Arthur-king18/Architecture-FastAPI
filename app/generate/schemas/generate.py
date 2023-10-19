from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    text_request: str | None = Field(alias="textRequest")
    theme: str | None
    theme_option: str | None = Field(alias="themeOption")


class BaseResponse(BaseModel):
    theme: str


class TextResponse(BaseResponse, BaseModel):
    text: str


class ImageResponse(BaseResponse, BaseModel):
    image_url: str
    light_background: str
    dark_background: str