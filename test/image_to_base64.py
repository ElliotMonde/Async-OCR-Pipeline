import base64
import sys

def image_to_base64(image_path: str) -> None:
    with open(image_path, "rb") as f:
        b64_image_str = base64.b64encode(f.read())
    print(b64_image_str)

if __name__ == "__main__":
    image_to_base64(sys.argv[1])
