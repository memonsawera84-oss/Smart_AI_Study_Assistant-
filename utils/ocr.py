import easyocr
from PIL import Image

# Load EasyOCR model only once
reader = easyocr.Reader(['en','ur'])


def extract_text_from_image(uploaded_image):
    """
    Extract text from an uploaded image using EasyOCR.
    """

    # Open image
    img = Image.open(uploaded_image)

    # OCR
    result = reader.readtext(
        img,
        detail=0,
        paragraph=True
    )

    # Convert list to string
    text = "\n".join(result)

    return text