# Samsung Frame TV Art Uploader

This script uploads an image to a Samsung Frame TV in Art Mode. The image is resized and cropped to fit the TV's aspect ratio, and then uploaded using the `samsungtvws` library.

Inspired by the [ow/samsung-frame-art](https://github.com/ow/samsung-frame-art) repo.

## Installation

1.  Clone this repository or download the `frame_tv_image.py` script.
2.  Install the necessary dependencies by running `pip3 install -r requirements.txt`.

## Usage

1.  Ensure that your Samsung Frame TV is turned on and connected to the same network as the computer running this script.
2.  Open the `frame_tv_image.py` script in a text editor.
3.  Replace the `'192.168.68.100'` string in line 33 with the IP address of your Samsung Frame TV. This IP address should be the local IP address of your TV on your home network. You can find the IP address in the TV's settings or by checking your router's connected devices list.
4.  Save the modified `frame_tv_image.py` script.
5.  Run the `frame_tv_image.py` script in a terminal or command prompt with `python3 frame_tv_image.py`.
6.  Enter the URL of the image you want to upload when prompted.
7.  The image will be uploaded to the TV and displayed in Art Mode.

## Limitations

- The script only works with Samsung Frame TVs in Art Mode.
- The image is cropped to fit the TV's aspect ratio, which may not always result in the desired composition.
- The script may not work with all image file types.

## Dependencies

The following Python libraries are required to run this script:

makefileCopy code

`opencv-python==4.5.4.58
numpy==1.19.5
Pillow==8.4.0
samsungtvws==2.2.2`

You can install the dependencies by running `pip install -r requirements.txt`.
