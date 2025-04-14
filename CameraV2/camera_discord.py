import requests
import picamera
import datetime
import os
from PIL import Image
import json

discord_webhook_url = "https://discord.com/api/webhooks/1361346984656503047/_DrOF__XM4YVyarqaa7S0n2deJUZjwnWX9qtxkajC2ZnXsbeQ0mbcQ00YELB5FJAhBXZ"

now = datetime.datetime.now()
dir_name = now.strftime('%Y%m%d')
dir_path = '/home/pi/github/raspberry-pi/CameraV2/' + dir_name
file_name = now.strftime('%H%M%S')

if not os.path.exists(dir_path):
    os.makedirs(dir_path)
os.chmod(dir_path, 0o777)

picamera = picamera.PiCamera()
picamera.resolution = (3280, 2464)
picamera.sharpness = 90
picamera.brightness = 42
picamera.exposure_mode = 'auto'
picamera.awb_mode = 'auto'
image_file = dir_path + '/' + file_name + '.jpg'
image_file_small = dir_path + '/' + file_name + '_small.jpg'
picamera.capture(image_file)

img = Image.open(image_file, 'r')
width, height = img.size
width = int(width * 0.8)
height = int(height * 0.8)
resize_img = img.resize((width, height))
resize_img.save(image_file_small)

with open(image_file_small, "rb") as f:
    files = {"file": (file_name + "_small.jpg", f, "image/jpeg")}
    payload = {
        "content": "Shot a picture of my room " + dir_name + " " + file_name
    }
    response = requests.post(discord_webhook_url, files=files, data=payload)

print(response.status_code)
print(response.content)

