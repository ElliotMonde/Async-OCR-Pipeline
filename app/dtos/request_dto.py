from pydantic import BaseModel
from typing import List

class ImageUploadRequestDto(BaseModel):
    image_data: str | List[str]