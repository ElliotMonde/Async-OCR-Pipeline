from fastapi import APIRouter, Depends
from dtos.response_dto import GetImageResponseDto, PostImageResponseDto
from api.services.ocr_service import OCRService
from dtos.request_dto import ImageUploadRequestDto
from shared.core.exceptions import NotFoundException
from shared.utils.helpers import process_base64_string

router = APIRouter(prefix="/image")


@router.get("/")
async def get_image(
    task_id: str, ocr_service: OCRService = Depends()
) -> GetImageResponseDto:
    '''
    Get OCR task result from database.
    Args:
        task_id (str): task id
    Returns:
        GetImageResponseDto: task response
    '''
    task_response: GetImageResponseDto = GetImageResponseDto(task_id=await ocr_service.get_task(task_id))
    return task_response


@router.post("/")
async def post_image(
    image_upload_request: ImageUploadRequestDto, ocr_service: OCRService = Depends()
) -> PostImageResponseDto:
    '''
    Queue OCR task into redis.
    Args:
        image_data (str | List[str]): base64 encoded image string or list of base64 encoded image strings
    Returns:
        PostImageResponseDto: task response
    '''
    if len(image_upload_request.image_data) == 0:
        raise NotFoundException(detail="Image data is empty")
    processed_image_data = image_upload_request.image_data
    task_response: PostImageResponseDto = PostImageResponseDto(task_id=await ocr_service.queue_task(processed_image_data))
    return task_response
