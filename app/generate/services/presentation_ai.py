import asyncio
import json
import random
import glob
import aiohttp
import base64
import ast

from datetime import datetime
from typing import Optional
from io import BytesIO

from core.config import EDEN_API
from app.generate.schemas.generate import CreateRequest
from app.generate.schemas.valid import ValidSlidesListResponseSchema
from app.generate.schemas.slide import GetSlidesListResponseSchema, ImageSchema
from core.exceptions import (
    PresentationNotGenerateException,
    TextNotGenerateException
)


EDEN_API = ast.literal_eval(EDEN_API)

class PresentationAI:
    def __init__(self, prompt: CreateRequest):
        self.headers = {"Authorization": []}
        self.request_url = "https://api.edenai.run/v2/{}/generation"
        self.payload_schema = {"providers": "openai"}
        self.theme = prompt.theme
        self.theme_option = prompt.theme_option
        self.textRequest = prompt.text_request
        self.service_text_request = "Classify the following prompt, detect how many slides user wants to create and the " \
                               "general subject and the general title. If you can't detect how many"\
                                "slides user wants, it should be 5."\
                               "But if the user wants to make more than 10 slides, then make 10 slides."\
                               "For each slide detect title and text. Then give me this " \
                               "data grouped with json format. Key for list of slides should be \"slides\"." \
                               "Follow the algorithm: at first detect subject and set it as value for \"subject\"." \
                               "At second detect title and set it as value for \"title\"."\
                               "Then, find information about subject and title and generate text about it and spread it across " \
                               "the slides, there should be at least 3 sentences for every slide, add \"title\" " \
                               f"and necessarily set value of \"bgColor\" to hex code of random {self.theme} color for slide in"\
                               "\"colors\". Enclose everything in "" json key "

        self.service_img_request = "{}, presentation style, ultra realistic, 4k"

        self.service_img_background_request = "background for slide, color is {}, 8k"


    async def generate(
            self,
            is_text: bool = True,
            slide_data: dict = None,
            user_prompt: str = None,
            is_background: bool = None,
            resolution: str = None,
            type_img: str = None,
            quantity: int = 1
    ):
        output = None
        try:
            if is_text:
                completion_prompt = f"{self.service_text_request}: {self.textRequest}"

                result = await self.send_request(
                    payload={"providers": "openai", "text": completion_prompt, "temperature" : 0.2, "max_tokens" : 1024},
                    is_text=is_text
                )

                output = await self.validation_text(result=result)

                if self.theme_option != "solid" and output is not None:
                    tasks = []
                    for key, slide_data in enumerate(output.get("slides")):
                        image_task = asyncio.create_task(self.generate(is_text=not is_text, slide_data=slide_data, is_background=False))
                        background_task = asyncio.create_task(self.generate(is_text=not is_text, slide_data=slide_data, is_background=True))
                        tasks += [image_task, background_task]
                        await asyncio.sleep(2) # limit api

                    await asyncio.gather(*tasks)

                    for (image, background_image), slide_data in zip(zip(tasks[::2], tasks[1::2]), output.get("slides")):
                        slide_data["image"] = await image
                        slide_data["image_path"] = slide_data["image"][0]["path"] if slide_data["image"] is not None else None

                        slide_data["image_background"] = await background_image
                        slide_data["image_background_path"] = slide_data["image_background"][0]["path"] if slide_data["image_background"] is not None else None

            else:
                try:
                    if not is_background:
                        prompt = self.service_img_request.format(
                            slide_data["title"]) if slide_data is not None else user_prompt
                        resolution = "512x512"
                    else:
                        prompt = self.service_img_background_request.format(
                            slide_data["bgColor"]) if slide_data is not None \
                            else user_prompt
                        resolution = "1024x1024"
                except Exception:
                    return None

                result = await self.send_request(
                    payload={"providers": "openai", "text": prompt, "resolution": resolution, "num_images": quantity},
                    is_text=is_text
                )

                return await self.validation_image(response=result, prompt=prompt, resolution=resolution, quantity=quantity)


        except Exception:
            raise PresentationNotGenerateException
        else:
            return output


    async def send_request(self, payload: dict, is_text: bool) -> json:

        async with aiohttp.ClientSession() as session:
            url = self.request_url.format("text") if is_text else self.request_url.format("image")
            self.headers["Authorization"] = random.choice(EDEN_API)

            response = await session.post(url, json=payload, headers=self.headers)
            if response.status == 200:
                result = await response.json()
                return result
            else:
                return None


    async def validation_text(self, result: json) -> json:
        try:
            data = result["openai"]["generated_text"]

            output = self.clear_data(data)
            ValidSlidesListResponseSchema.parse_raw(json.dumps(output))
        except Exception as e:
            return await self.generate(is_text=True)

        output["prompt"] = self.textRequest
        if output["subject"] is None:
            output["subject"] = output.get("slides")[0]["title"]

        return output


    async def validation_image(
            self,
            quantity: int = 1,
            type_img: str = "jpg",
            resolution: str = "512x512",
            prompt: str = None,
            response: str = None
        ) -> ImageSchema:
        result_list = []
        if response is not None:
            for i in range(quantity):
                    try:
                        image_file = BytesIO(base64.b64decode(response['openai']['items'][i]["image"]))
                    except KeyError:
                        return None

                    create_at = datetime.now()
                    file_path = f"pictures/image_{create_at}.{type_img}"
                    with open(f"{file_path}", "wb") as f:
                        f.write(image_file.read())

                    result = {
                        "source": "openai",
                        "prompt": prompt,
                        "resolution": resolution,
                        "type": type_img,
                        "path": file_path,
                        "create_at": create_at
                    }

                    result_list.append(result)

            return result_list
        else:
            return None


    @staticmethod
    def clear_data(data):
        start_index = data.index("{")
        end_index = data.rindex("}") + 1
        cleaned_data = data[start_index:end_index]
        output = json.loads(cleaned_data)

        return output