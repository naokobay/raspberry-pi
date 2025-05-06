# discord_camera_bot.py
import discord
import os
import datetime
import asyncio
import picamera
from PIL import Image

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
CAMERA_DIR = "/home/pi/photos"
RESIZE_SCALE = 1.0

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d'), now.strftime('%H%M%S')

def prepare_directory(date_str):
    dir_path = os.path.join(CAMERA_DIR, date_str)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    os.chmod(dir_path, 0o777)
    return dir_path

def capture_image(path):
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.capture(path)

def resize_image(src_path, dst_path):
    img = Image.open(src_path)
    width, height = img.size
    new_size = (int(width * RESIZE_SCALE), int(height * RESIZE_SCALE))
    resized = img.resize(new_size)
    resized.save(dst_path)

@client.event
async def on_ready():
    print("[INFO] Bot connected as {}".format(client.user.name))

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    if "撮って" in content or "take photo" in content or "photo" in content:
        await message.channel.send("📸 撮影します…")

        date_str, time_str = get_timestamp()
        dir_path = prepare_directory(date_str)
        original = os.path.join(dir_path, time_str + ".jpg")
        resized = os.path.join(dir_path, time_str + "_small.jpg")

        try:
            capture_image(original)
            resize_image(original, resized)
            await message.reply(file=discord.File(resized), mention_author=True)
        except Exception as e:
            await message.channel.send("😢 撮影に失敗しました: {}".format(e))

client.run(TOKEN)

