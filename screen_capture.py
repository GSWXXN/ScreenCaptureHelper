import sys

from PyQt5.QtGui import QPixmap, QGuiApplication, QColor, QPen, QPainter
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, qAbs, QRect, QPoint


def get_rect(beginPoint, endPoint):
    width = qAbs(beginPoint.x() - endPoint.x())
    height = qAbs(beginPoint.y() - endPoint.y())
    x = beginPoint.x() if beginPoint.x() < endPoint.x() else endPoint.x()
    y = beginPoint.y() if beginPoint.y() < endPoint.y() else endPoint.y()
    selected_rect = QRect(x, y, width, height)
    # 避免宽或高为零时拷贝截图有误
    # 可以看QQ截图，当选取截图宽或高为零时默认为2
    if selected_rect.width() == 0:
        selected_rect.setWidth(1)
    if selected_rect.height() == 0:
        selected_rect.setHeight(1)
    return selected_rect


class CaptureScreen(QWidget):
    """
    截屏: 使用时仅需直接new一个该实例即可出现全屏的截屏界面
    """
    load_pixmap = None
    screen_width = None
    screen_height = None
    is_mouse_pressed = None
    begin_pos = None
    end_pos = None
    upper_left_pos = None
    capture_pixmap = None
    bhv = None
    painter = QPainter()
    signal_complete_capture = pyqtSignal(QPixmap, QPoint, int)

    def __init__(self):
        QWidget.__init__(self)
        self.init_window()
        self.load_background_pixmap()
        self.setCursor(Qt.CrossCursor)
        self.show()

    def init_window(self):
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen)
        self.setWindowState(Qt.WindowActive | Qt.WindowFullScreen)

    def load_background_pixmap(self):
        # 截下当前屏幕的图像
        self.load_pixmap = QGuiApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
        self.screen_width = self.load_pixmap.width()
        self.screen_height = self.load_pixmap.height()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = True
            self.begin_pos = event.pos()
        if event.button() == Qt.RightButton:
            sys.exit()
        return QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.is_mouse_pressed is True:
            self.end_pos = event.pos()
            self.update()
        return QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.end_pos = event.pos()
        self.upper_left_pos = QPoint(min(self.begin_pos.x(), self.end_pos.x()),
                                     min(self.begin_pos.y(), self.end_pos.y()))
        self.is_mouse_pressed = False

        return QWidget.mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        sys.exit()

    def paintEvent(self, event):
        self.painter.begin(self)
        shadow_color = QColor(0, 0, 0, 100)  # 阴影颜色设置
        self.painter.setPen(QPen(Qt.gray, 1, Qt.SolidLine, Qt.FlatCap))  # 设置画笔
        self.painter.drawPixmap(0, 0, self.load_pixmap)  # 将背景图片画到窗体上
        self.painter.fillRect(self.load_pixmap.rect(), shadow_color)  # 画影罩效果
        if self.is_mouse_pressed:
            selected_rect = get_rect(self.begin_pos, self.end_pos)
            self.capture_pixmap = self.load_pixmap.copy(selected_rect)
            self.painter.drawPixmap(selected_rect.topLeft(), self.capture_pixmap)
            self.painter.drawRect(selected_rect)
        self.painter.end()  # 重绘结束

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            sys.exit()

        if (event.key() in [Qt.Key_O, Qt.Key_S, Qt.Key_M]) \
                and self.capture_pixmap is not None:
            self.signal_complete_capture.emit(self.capture_pixmap, self.upper_left_pos, event.key())
            self.close()
