#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ファイル名: led.py

import RPi.GPIO as GPIO
import time

# 初期設定
# GPIO.BOARD: PIN番号
# GPIO.BCM:   GPIO番号
GPIO.setmode(GPIO.BCM)

contRed =   17
contGreen = 23
contBlue =  27
contON =    0
contOFF =   1

GPIO.setup( contRed,   GPIO.OUT )
GPIO.setup( contGreen, GPIO.OUT )
GPIO.setup( contBlue,  GPIO.OUT )

# サブルーチン
def led( intR, intG, intB ):
    GPIO.output( contRed,   intR )
    GPIO.output( contGreen, intG )
    GPIO.output( contBlue,  intB )
    time.sleep(1)

# メインルーチン
if __name__ == '__main__':

    try:
        while True:
            # 1秒毎に赤、緑、青の点灯を繰り返す
            led( contON, contOFF, contOFF)
            led( contOFF, contON, contOFF)
            led( contOFF, contOFF, contON)

    finally:
        # GPIOを解放して終了。
        GPIO.cleanup()
