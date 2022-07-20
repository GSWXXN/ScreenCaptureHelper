import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QBuffer, QByteArray, QIODevice

import screenshot
from sticker import Sticker
from screen_capture import CaptureScreen
import ocr


def pixmap_to_bytes(image, image_format='bmp'):
    """
    Pixmap转字节
    :param image: pixmap
    :param image_format: str
    :return: bytes
    """
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)
    image.save(buffer, image_format)
    return buffer.data()


@pyqtSlot(QPixmap, QPoint, int)
def __slot_screen_capture(image, point, key):
    image_bytes = pixmap_to_bytes(image)
    if key == Qt.Key_O:
        sticker.close()
        ocr.start(image_bytes)
    elif key == Qt.Key_S:
        sticker.close()
        screenshot.start(image_bytes)
    elif key == Qt.Key_M:
        sticker.setup_ui(image, point)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    capture = CaptureScreen()
    sticker = Sticker()
    capture.signal_complete_capture.connect(__slot_screen_capture)
    sys.exit(app.exec_())
