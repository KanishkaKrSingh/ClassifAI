from pdf2image import convert_from_path
import os

# Input PDF path
input_pdf = "JEE_Main_2002.pdf"  # 🔁 change this to your test PDF path
output_image = "page_sample.png"

# Convert first page only
images = convert_from_path(input_pdf, dpi=300, first_page=1, last_page=1)
images[0].save(output_image, "PNG")

print("✅ PDF page converted to image:", output_image)

import cv2
import numpy as np

# Load the image
img = cv2.imread("page_sample.png")

# Step 1: Increase brightness and contrast
bright = cv2.convertScaleAbs(img, alpha=1.3, beta=50)  # alpha=contrast, beta=brightness

# Step 2: Convert to grayscale
gray = cv2.cvtColor(bright, cv2.COLOR_BGR2GRAY)

# Step 3: Binarize to clean up watermark
_, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

# Save result
cv2.imwrite("page_cleaned.png", binary)

print("✅ Watermark-faded version saved: page_cleaned.png")

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

original = cv2.cvtColor(cv2.imread("page_sample.png"), cv2.COLOR_BGR2RGB)
cleaned = cv2.cvtColor(cv2.imread("page_cleaned.png"), cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Original")
plt.imshow(original)
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("Cleaned")
plt.imshow(cleaned)
plt.axis("off")

plt.tight_layout()
plt.show()
