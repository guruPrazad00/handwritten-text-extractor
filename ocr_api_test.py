import requests

# Your OCR.Space API Key
API_KEY = "K81311603388957"

# Image path
image_path = "sample.jpg"

# OCR.Space endpoint
url_api = "https://api.ocr.space/parse/image"

# Open image
with open(image_path, 'rb') as image_file:

    response = requests.post(
        url_api,
        files={
            "filename": image_file
        },
        data={
            "apikey": API_KEY,
            "language": "eng",
            "isOverlayRequired": False,
            "OCREngine": 2
        }
    )

# Convert response to JSON
result = response.json()

print("\nRecognized Text:\n")

# Extract text
parsed_text = result['ParsedResults'][0]['ParsedText']

print(parsed_text)
