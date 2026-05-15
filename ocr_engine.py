import requests
import cv2
import os

# Replace with your OCR.Space API key
API_KEY = "K81311603388957"


def extract_text_and_overlay(image_path):

    url_api = "https://api.ocr.space/parse/image"

    with open(image_path, 'rb') as image_file:

        response = requests.post(
            url_api,
            files={
                "filename": image_file
            },
            data={
                "apikey": API_KEY,
                "language": "eng",
                "isOverlayRequired": True,
                "OCREngine": 2
            }
        )

    result = response.json()

    print(result)

    try:

        parsed_result = result['ParsedResults'][0]

        parsed_text = parsed_result['ParsedText']

        overlay_lines = parsed_result['TextOverlay']['Lines']

    except Exception as e:

        print("ERROR:", e)

        return "OCR failed.", None

    # Load image
    img = cv2.imread(image_path)

    # Process detected words
    for line in overlay_lines:

        words = line['Words']

        for word in words:

            x = int(word['Left'])
            y = int(word['Top'])
            w = int(word['Width'])
            h = int(word['Height'])

            # Skip huge decorative text
            if w > 140 or h > 60:
                continue

            # Smaller blur region
            padding = 4

            x1 = max(x + padding, 0)
            y1 = max(y + padding, 0)

            x2 = min(x + w - padding, img.shape[1])
            y2 = min(y + h - padding, img.shape[0])

            # Crop word region
            roi = img[y1:y2, x1:x2]

            # Skip empty regions
            if roi.size == 0:
                continue

            # Blur handwritten word
            blurred = cv2.GaussianBlur(
                roi,
                (25, 25),
                0
            )

            img[y1:y2, x1:x2] = blurred

            # Dynamic font scaling
            font_scale = max(h / 40, 0.45)

            # Overlay OCR text
            cv2.putText(
                img,
                word['WordText'],
                (x, y + h - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                (0, 0, 0),
                1,
                cv2.LINE_AA
            )

    # Save processed image
    output_filename = "processed_output.jpg"

    output_path = os.path.join(
        "static/uploads",
        output_filename
    )

    cv2.imwrite(output_path, img)

    return parsed_text, output_filename