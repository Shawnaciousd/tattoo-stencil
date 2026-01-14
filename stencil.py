import cv2
import numpy as np
from PIL import Image
import io

def generate_stencil(image_bytes, line_thickness=2):
    # Load image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Increase contrast
    gray = cv2.equalizeHist(gray)

    # Edge detection
    edges = cv2.Canny(gray, 80, 160)

    # Thicken lines
    kernel = np.ones((line_thickness, line_thickness), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # Remove small noise
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    clean = np.zeros_like(edges)

    for c in contours:
        if cv2.contourArea(c) > 100:
            cv2.drawContours(clean, [c], -1, 255, thickness=1)

    # Invert to black lines on white
    stencil = cv2.bitwise_not(clean)

    # Mirror image for stencil transfer
    stencil = cv2.flip(stencil, 1)

    # Convert to PNG
    result = Image.fromarray(stencil)
    output = io.BytesIO()
    result.save(output, format="PNG")
    output.seek(0)

    return output
