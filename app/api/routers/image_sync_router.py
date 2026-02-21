from fastapi import APIRouter, Depends, Form
from api.services.ocr_service import OCRService
from dtos.response_dto import SyncImageResponseDto
from dtos.request_dto import ImageUploadRequestDto
from typing import List
from shared.utils.helpers import process_base64_string

router = APIRouter()

@router.post("/image-sync")
def sync_upload_image(image_upload_request: ImageUploadRequestDto, ocr_service: OCRService = Depends()) -> SyncImageResponseDto:
    '''
    Synchronously upload image as base64 string and return OCR text
    Args:
        image_data (str): base64 encoded image string
    Returns:
        SyncImageResponseDto: task response
    '''
    processed_image_data = []
    if isinstance(image_upload_request.image_data, List):
        for i in range(len(image_upload_request.image_data)):
            processed_image_data.append(process_base64_string(image_upload_request.image_data[i]))
    else:
        processed_image_data = [image_upload_request.image_data]
    text: str | List[str] = ocr_service.sync_upload_image(processed_image_data)
    return SyncImageResponseDto(text=text)