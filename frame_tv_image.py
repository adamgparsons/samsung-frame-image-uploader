import sys
import logging
import os
import json
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import urllib.request

from samsungtvws import SamsungTVWS

def download_image(url):
    try:
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        return Image.open(BytesIO(image_data))
    except Exception as e:
        print(f"Error downloading or opening image: {e}")
        return None

def spectral_residual_saliency(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.resize(gray_image, (160, 160), interpolation=cv2.INTER_LINEAR)
    myFFT = cv2.dft(np.float32(gray_image), flags=cv2.DFT_COMPLEX_OUTPUT)
    amplitude, phase = cv2.cartToPolar(myFFT[..., 0], myFFT[..., 1])

    normalized_log_amplitude = cv2.boxFilter(np.log10(amplitude), -1, (3, 3), normalize=True)
    spectral_residual = np.log10(amplitude) - normalized_log_amplitude

    myIFFT = cv2.idft(np.float32(np.exp(cv2.polarToCart(spectral_residual, phase)[0])), flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
    saliency = cv2.GaussianBlur(myIFFT, (5, 5), 3)
    saliency = cv2.resize(saliency, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_LINEAR)

    return saliency

def resize_and_crop(image, size, ratio):
    width, height = image.size
    target_width, target_height = size

    cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    saliency_map = spectral_residual_saliency(cv2_image)
    y_min, y_max, x_min, x_max = cv2.boundingRect(np.uint8(saliency_map > saliency_map.mean()))

    salient_width = x_max - x_min
    salient_height = y_max - y_min

    if width / height > ratio:
        new_width = int(height * ratio)
        left = x_min - (new_width - salient_width) // 2
        right = left + new_width

        if left < 0:
            right += abs(left)
            left = 0
        if right > width:
            left -= right - width
            right = width

        image = image.crop((left, 0, right, height))
    else:
        new_height = int(width / ratio)
        top = y_min - (new_height - salient_height) // 2
        bottom = top + new_height

        if top < 0:
            bottom += abs(top)
            top = 0
        if bottom > height:
            top -= bottom - height
            bottom = height

        image = image.crop((0, top, width, bottom))

    return image.resize(size)

def main():
    logging.basicConfig(level=logging.INFO)

    # Set your TVs local IP address. Highly recommend using a static IP address for your TV.
    tv = SamsungTVWS('192.168.68.100')

    # Checks if the TV supports art mode
    art_mode = tv.art().supported()

    if art_mode == True:
        image_url = input("Enter the image URL: ")
        image = download_image(image_url)


        if image:
            image = resize_and_crop(image, (1920, 1080), 16/9)
            image_data = BytesIO()
            image.save(image_data, format='JPEG')
            image_data.seek(0)

            # Upload the image to the TV and select it as the current art
            remote_filename = tv.art().upload(image_data.read(), file_type='JPEG', matte="none")
            tv.art().select_image(remote_filename, show=True)
            print("Image has been sent to your Samsung Frame TV.")
        else:
            print("Failed to download the image. Please check the URL and try again.")
    else:
        logging.warning('Your TV does not support art mode.')

if __name__ == "__main__":
    main()