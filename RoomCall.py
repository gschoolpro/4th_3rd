# -*- coding: utf-8 -*-
import requests
import RPi.GPIO as GPIO
import time

# ボタンスイッチ関連変数
inPin = 14  # ボタンスイッチ入力ポート
preIn = 0


def setupGpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(inPin, GPIO.IN)


# IFTTTに送信する関数
def sendIfttt(eventName, area, iftttKey):
    # dataBoxの値がIFTTTに渡されます
    dataBox = {"value1": area,
               "value2": None,
               "value3": None}
    url = "https://maker.ifttt.com/trigger/" + eventName + "/with/key/" + iftttKey
    res = requests.post(url, data=dataBox)  # ここで送信されます
    return res


def destroy():
    GPIO.cleanup()


if __name__ == "__main__":
    print("セットアップを開始します...")
    eventName = "RoomCall"  # イベント名を指定
    iftttKey = "XXXXXXXXXXXXXXX"  # キーを入力
    area = "リビング"  # IFTTTに渡す値

    setupGpio()

    print("セットアップが完了しました")
    try:
        while True:
            curIn = GPIO.input(inPin)
            if(preIn == 0):
                if(GPIO.input(inPin) == 1):
                    print("IFTTTに送信しています...")
                    res = sendIfttt(eventName, area, iftttKey)
                    if(res.status_code == 200):
                        print("通知の送信に成功しました")
                    else:
                        print("通知の送信に失敗しました...")
            preIn = curIn
            time.sleep(0.2)
    except KeyboardInterrupt:
        destroy()
