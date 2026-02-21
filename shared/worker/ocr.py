import pytesseract
from PIL import Image
from io import BytesIO
import base64


class OCR:
    def __init__(self):
        self.ocr = pytesseract.pytesseract

    def ocr_from_b64(self, b64_image: str) -> str:
        """
        Perform OCR on the given image.

        Args:
            b64_image: Base64 encoded image string

        Returns:
            str: OCR result
        """
        image = Image.open(BytesIO(base64.b64decode(b64_image)))
        text = pytesseract.image_to_string(image)
        return text

    def ocr_from_bytes(self, image_bytes: bytes) -> str:
        """
        Perform OCR on the given image.

        Args:
            image_bytes: Image bytes

        Returns:
            str: OCR result
        """
        image = Image.open(BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
