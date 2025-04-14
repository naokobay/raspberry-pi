import picamera
import datetime
import os
 
now = datetime.datetime.now()
dir_name = now.strftime('%Y%m%d')
dir_path = '/home/pi/github/raspberry-pi/CameraV2/'+dir_name
file_name = now.strftime('%H%M%S')
 
if not os.path.exists(dir_path):
	os.makedirs(dir_path)
os.chmod(dir_path, 0777)
 
picamera = picamera.PiCamera()
picamera.resolution = (3280,2464)
picamera.sharpness = 100
picamera.brightness = 42
picamera.exposure_mode = 'auto'
picamera.awb_mode = 'auto'
picamera.capture(dir_path+'/'+file_name+'.jpg')

