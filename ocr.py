import os
import sys
import threading
import time

import pyperclip
import requests
from aip import AipOcr
from win10toast import ToastNotifier

# 认证信息
APP_ID = '****'
API_KEY = '*****'
SECRET_KEY = '****'


def get_ocr_str_from_bytes(file_bytes, origin_format=True):
    """
    图片转文字
    :param file_bytes: 图片的字节
    :param origin_format: 多行文本是否换行
    :return:
    """
    options = {
        'detect_direction': 'false',
        'language_type': 'CHN_ENG',
    }
    ocr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    result_dict = ocr.basicGeneral(file_bytes, options)
    if origin_format:
        result_str = '\n'.join([entity['words'] for entity in result_dict['words_result']])
    else:
        result_str = ''.join([entity['words'] for entity in result_dict['words_result']])
    return result_str


def job_ocr(image_bytes):
    result = ''
    status = '错误 !!!!!'
    try:
        result = get_ocr_str_from_bytes(image_bytes)
    except requests.exceptions.ConnectionError:
        result = "无网络"
    except Exception as err:
        result = err
    else:
        pyperclip.copy(result)
        status = '结果'
    finally:
        print(result)
        toaster = ToastNotifier()
        toaster.show_toast("OCR 识别" + status,
                           str(result),
                           icon_path=os.path.join(os.getcwd(), get_resource_path('./asset/icon.ico')),
                           duration=5,
                           threaded=False)
        while toaster.notification_active():
            time.sleep(0.1)


def run_ocr_async(image_bytes):
    threading.Thread(target=job_ocr, args=(image_bytes,)).start()


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def start(image_bytes):
    if image_bytes is None or len(image_bytes) == 0:
        return
    run_ocr_async(image_bytes)
