# -*- coding: utf-8 -*-
"""Image Enhancement: Arithmetic/Logic Operations.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iA8aSnS6lPtUYWh4HvfQqP1q20VWiSQA
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

video = cv2.VideoCapture("/content/sample_video.mp4")
success, frame1 = video.read()  # First frame
success, frame2 = video.read()  # Second frame
video.release()

frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

# image subtraction
change_detected = cv2.absdiff(frame1_gray, frame2_gray)

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.title("Frame 1 (Before)")
plt.imshow(frame1_gray, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title("Frame 2 (After)")
plt.imshow(frame2_gray, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title("Change Detected")
plt.imshow(change_detected, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()

import cv2
import matplotlib.pyplot as plt
import requests
import numpy as np

# Function to load an image from a URL
def load_image_from_url(url):
    response = requests.get(url)
    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return img

# Load the base image and the watermark image
base_image_url = 'https://picsum.photos/300/300'  # Example base image URL
watermark_image_url = 'https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png'  # Instagram logo URL

base_image = load_image_from_url(base_image_url)
watermark_image = load_image_from_url(watermark_image_url)

# Resize watermark to fit the base image
watermark_image = cv2.resize(watermark_image, (base_image.shape[1], base_image.shape[0]))

# Ensure images are in the uint8 type for proper display
base_image = np.array(base_image, dtype=np.uint8)
watermark_image = np.array(watermark_image, dtype=np.uint8)

# Parameters for watermarking
alpha = 1
beta = 0.1
gamma = 0

# Apply watermarking by blending the images
watermarked_image = cv2.addWeighted(base_image, alpha, watermark_image, beta, gamma)

# Show the watermarked image
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(watermarked_image, cv2.COLOR_BGR2RGB))
plt.title('Watermarked Image')
plt.axis('off')

# Recover the original image from the watermarked image (invert the watermarking process)
recovered_image = cv2.addWeighted(watermarked_image, 1/alpha, watermark_image, -beta/alpha, -gamma/alpha)

# Show the recovered image
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(recovered_image, cv2.COLOR_BGR2RGB))
plt.title('Recovered Image')
plt.axis('off')

plt.tight_layout()
plt.show()

import cv2
import numpy as np

# Load the original image
image_path = '/content/Lenna_(test_image).png'
image = cv2.imread(image_path, cv2.IMREAD_COLOR)

if image is None:
    raise ValueError(f"Unable to load image. Check the file path: {image_path}")

# Function to add Gaussian noise
def add_gaussian_noise(image, mean=0, sigma=25):
    row, col, ch = image.shape
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    noisy = np.add(image, gauss).astype(np.uint8)
    return noisy

# Function to add salt-and-pepper noise
def add_salt_and_pepper_noise(image, salt_prob=0.01, pepper_prob=0.01):
    noisy = np.copy(image)
    total_pixels = image.size
    num_salt = int(salt_prob * total_pixels)
    num_pepper = int(pepper_prob * total_pixels)

    # Salt noise (random white pixels)
    salt_coords = [np.random.randint(0, i-1, num_salt) for i in image.shape]
    noisy[salt_coords[0], salt_coords[1], :] = 255

    # Pepper noise (random black pixels)
    pepper_coords = [np.random.randint(0, i-1, num_pepper) for i in image.shape]
    noisy[pepper_coords[0], pepper_coords[1], :] = 0

    return noisy

# Function to add Poisson noise
def add_poisson_noise(image):
    noisy = np.random.poisson(image.astype(float) / 255) * 255
    return np.clip(noisy, 0, 255).astype(np.uint8)

# Function to add speckle noise
def add_speckle_noise(image):
    row, col, ch = image.shape
    speckle = np.random.normal(0, 0.1, (row, col, ch))
    noisy = np.add(image, image * speckle)
    return np.clip(noisy, 0, 255).astype(np.uint8)

# Save the noisy images to files
noisy_images = {
    'Gaussian': add_gaussian_noise(image),
    'Salt_and_Pepper': add_salt_and_pepper_noise(image),
    'Poisson': add_poisson_noise(image),
    'Speckle': add_speckle_noise(image)
}

for noise_type, noisy_image in noisy_images.items():
    file_path = f'/content/{noise_type}_noisy_image.png'
    cv2.imwrite(file_path, noisy_image)

print("Noisy images saved successfully.")

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the noisy images from files
noisy_images_files = [
    '/content/Gaussian_noisy_image.png',
    '/content/Salt_and_Pepper_noisy_image.png',
    '/content/Speckle_noisy_image.png'
]

# Function to load images from file paths
def load_images(file_paths):
    images = [cv2.imread(file_path) for file_path in file_paths]
    return images

# Load all noisy images
noisy_images = load_images(noisy_images_files)

# Average the noisy images
def average_images(images):
    return np.mean(images, axis=0).astype(np.uint8)

# Average the loaded noisy images
average_image = average_images(noisy_images)

# Plot the averaged image
plt.figure(figsize=(8, 6))
plt.title('Averaged Image')
plt.imshow(cv2.cvtColor(average_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()