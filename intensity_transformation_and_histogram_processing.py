# -*- coding: utf-8 -*-
"""Intensity Transformation and Histogram Processing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j-kh9I0EF81I7JvRmv_gYCOZTCdwCh1D
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the input image
image_path = '/content/Rainier.png'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Create a reference image by applying histogram equalization
reference_image = cv2.equalizeHist(gray_image)

# Display the original grayscale image and the reference image
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(gray_image, cmap='gray')
axes[0].set_title('Grayscale Image')
axes[1].imshow(reference_image, cmap='gray')
axes[1].set_title('Reference Image (Histogram Equalized)')

plt.tight_layout()
plt.show()

# Save the reference image
cv2.imwrite('/content/reference_image.png', reference_image)

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load grayscale image
image = cv2.imread('/content/Rainier.png', cv2.IMREAD_GRAYSCALE)

# Histogram Equalization
equalized_image = cv2.equalizeHist(image)

# Histogram Matching (Assume we have a reference image)
reference_image = cv2.imread('/content/reference_image.png', cv2.IMREAD_GRAYSCALE)
# Perform histogram matching using skimage or another technique
from skimage import exposure
matched_image = exposure.match_histograms(image, reference_image, channel_axis=None)

# Compute Entropy (a measure of information content)
def compute_entropy(img):
    hist, _ = np.histogram(img, bins=256, range=(0, 256))
    hist = hist / hist.sum()
    entropy = -np.sum(hist * np.log2(hist + 1e-6))  # Adding small value to avoid log(0)
    return entropy

# Entropy of the original, equalized, and matched images
entropy_original = compute_entropy(image)
entropy_equalized = compute_entropy(equalized_image)
entropy_matched = compute_entropy(matched_image)

# Displaying images and entropy values
fig, axes = plt.subplots(1, 4, figsize=(15, 5))
axes[0].imshow(image, cmap='gray')
axes[0].set_title('Original Image')
axes[1].imshow(equalized_image, cmap='gray')
axes[1].set_title(f'Equalized (Entropy: {entropy_equalized:.3f})')
axes[2].imshow(matched_image, cmap='gray')
axes[2].set_title(f'Matched (Entropy: {entropy_matched:.3f})')
axes[3].hist(image.ravel(), bins=256, range=(0, 256), color='r', alpha=0.7)
axes[3].hist(equalized_image.ravel(), bins=256, range=(0, 256), color='g', alpha=0.7)
axes[3].hist(matched_image.ravel(), bins=256, range=(0, 256), color='b', alpha=0.7)
axes[3].set_title('Histograms')

plt.tight_layout()
plt.show()

# Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
clahe_image = clahe.apply(image)

# Display original and enhanced images
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(image, cmap='gray')
axes[0].set_title('Original Low Contrast Image')
axes[1].imshow(clahe_image, cmap='gray')
axes[1].set_title('Enhanced (CLAHE) Image')

plt.tight_layout()
plt.show()

from skimage.metrics import structural_similarity as ssim
mse = np.sum((image - clahe_image) ** 2) / float(image.shape[0] * image.shape[1])
ssim_value = ssim(image, clahe_image)

print(f'MSE: {mse:.3f}, SSIM: {ssim_value:.3f}')