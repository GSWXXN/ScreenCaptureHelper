import sys
from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsDropShadowEffect, QGridLayout, QMainWindow
from PyQt5.QtCore import Qt


class Sticker(QMainWindow):
    alpha = 1
    scale = 0.04
    min_alpha = 0.15
    shadow_radius = 15

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.ismoving = True
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()
        if e.button() == Qt.RightButton:
            sys.exit()

    def mouseMoveEvent(self, e):
        if self.ismoving:
            relpos = e.globalPos() - self.start_point
            self.move(self.window_point + relpos)

    def mouseReleaseEvent(self, e):
        self.ismoving = False

    def wheelEvent(self, event):
        delta = event.angleDelta()
        orientation = delta.y() / 8
        if orientation > 0:
            self.alpha += self.scale
            if self.alpha > 1:
                self.alpha = 1
            self.setWindowOpacity(self.alpha)
        else:
            self.alpha -= self.scale
            if self.alpha < self.min_alpha:
                self.alpha = self.min_alpha
            self.setWindowOpacity(self.alpha)

    def setup_ui(self, image, point):
        self.setWindowOpacity(self.alpha)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)
        self.setFixedSize(image.width() + self.shadow_radius * 3 / 2, image.height() + self.shadow_radius * 3 / 2)
        self.move(point.x() - self.shadow_radius * 4 / 5, point.y() - self.shadow_radius * 4 / 5)

        self.main_widget = QWidget()
        self.main_widget.setStyleSheet('''QWidget{border-radius:7px;background-color:rgb(255,255,255);}''')
        self.add_shadow()

        self.base_widget = QWidget()  # 创建透明窗口
        self.base_widget.setStyleSheet('''QWidget{  border-radius:7px;background-color:rgb(255, 255, 255);}''')
        self.base_widget.setObjectName('base_widget')
        self.base_layout = QGridLayout()
        self.base_widget.setLayout(self.base_layout)
        self.base_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.setCentralWidget(self.base_widget)  # 设置窗口主部件
        self.base_layout.addWidget(self.main_widget)

        self.lb1 = QLabel(self.main_widget)
        self.lb1.setGeometry(0, 0, image.width(), image.height())
        self.lb1.setPixmap(image)

        self.show()

    def add_shadow(self):
        # 添加阴影
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(self.shadow_radius)  # 阴影半径
        self.effect_shadow.setColor(Qt.gray)  # 阴影颜色
        self.main_widget.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中
