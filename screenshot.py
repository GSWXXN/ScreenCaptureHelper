import os
import time

import win32clipboard as clip
import win32con
import winreg

from win10toast import ToastNotifier

from ocr import get_resource_path


def clipboard(image):
    image = image[14:]
    clip.OpenClipboard()  # 打开剪贴板
    clip.EmptyClipboard()  # 先清空剪贴板
    clip.SetClipboardData(win32con.CF_DIB, image)  # 将图片放入剪贴板
    clip.CloseClipboard()


def save_img(image):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders')
    value, type = winreg.QueryValueEx(key, "Desktop")
    path = value + '\\ScreenShot' + time.strftime("%Y-%m-%d %H_%M_%S", time.localtime()) + ".png"
    print(path)

    with open(path, 'wb') as f:
        f.write(image)


def start(image):
    clipboard(image)
    save_img(image)
    toaster = ToastNotifier()
    toaster.show_toast('截图',
                       '截图已保存到桌面并复制到剪贴板',
                       icon_path=os.path.join(os.getcwd(), get_resource_path('./asset/screenshot.ico')),
                       duration=5,
                       threaded=True)

