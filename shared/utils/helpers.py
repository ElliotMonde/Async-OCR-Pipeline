import base64

def process_base64_string(base64_string: str) -> str:
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]

    return base64_string

