import os
import datetime
import requests
from PIL import Image
import picamera

BASE_DIR = '/home/pi/github/raspberry-pi/CameraV2'
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1361346984656503047/_DrOF__XM4YVyarqaa7S0n2deJUZjwnWX9qtxkajC2ZnXsbeQ0mbcQ00YELB5FJAhBXZ"
CAMERA_RESOLUTION = (3280, 2464)
CAMERA_SHARPNESS = 90
CAMERA_BRIGHTNESS = 30
RESIZE_SCALE = 1.0


def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d'), now.strftime('%H%M%S')


def prepare_directory(date_str):
    dir_path = os.path.join(BASE_DIR, date_str)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    os.chmod(dir_path, 0o777)
    return dir_path


def capture_image(camera, path):
    try:
        camera.capture(path)
        print("[INFO] Captured image: {}".format(path))
    except Exception as e:
        print("[ERROR] Failed to capture image: {}".format(e))
        raise


def resize_image(src_path, dst_path, scale=1.0):
    try:
        img = Image.open(src_path)
        width, height = img.size
        new_size = (int(width * scale), int(height * scale))
        resized = img.resize(new_size)
        resized.save(dst_path)
        print("[INFO] Resized image saved: {}".format(dst_path))
    except Exception as e:
        print("[ERROR] Failed to resize image: {}".format(e))
        raise


def send_to_discord(image_path, message):
    try:
        with open(image_path, "rb") as f:
            files = {"file": (os.path.basename(image_path), f, "image/jpeg")}
            payload = {"content": message}
            response = requests.post(DISCORD_WEBHOOK_URL, files=files, data=payload)
            response.raise_for_status()
            print("[INFO] Sent image to Discord: {}".format(response.status_code))
    except Exception as e:
        print("[ERROR] Failed to send image to Discord: {}".format(e))
        raise


def main():
    date_str, time_str = get_timestamp()
    dir_path = prepare_directory(date_str)
    image_path = os.path.join(dir_path, "{}.jpg".format(time_str))
    resized_path = os.path.join(dir_path, "{}_small.jpg".format(time_str))

    camera = picamera.PiCamera()
    try:
        camera.resolution = CAMERA_RESOLUTION
        camera.sharpness = CAMERA_SHARPNESS
        camera.brightness = CAMERA_BRIGHTNESS
	camera.contrast = 5
	camera.saturation = 5
        camera.exposure_mode = 'auto'
        camera.awb_mode = 'auto'

        capture_image(camera, image_path)
#        resize_image(image_path, resized_path, RESIZE_SCALE)
#        send_to_discord(resized_path, "Shot a picture of my room {} {}".format(date_str, time_str))
        send_to_discord(image_path, "Shot a picture of my room {} {}".format(date_str, time_str))

    finally:
        camera.close()


if __name__ == "__main__":
    main()

