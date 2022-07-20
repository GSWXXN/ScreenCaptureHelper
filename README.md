# Screen Capture Helper
屏幕捕捉助手

## OCR相关
脚本使用[百度 OCR API](https://ai.baidu.com/tech/ocr), 使用源码前请先配置 [ocr.py](/ocr.py) 中的认证信息。

## 使用说明
启动后框选屏幕区域
* 按下 O 键，进项 OCR 识别文字，识别成功后自动复制到剪切板
* 按下 S 键，截图并保存到桌面
* 按下 M 键，进入贴图模式
    * 在贴图上滑动鼠标滚轮调整透明度
    * 拖动移动贴图位置
    * 在贴图上单击鼠标右键退出贴图模式

## 建议使用方式
由于程序在未使用时不会在后台停留，可以配合手势软件如 [MouseInc](https://shuax.com/) 、[WGestures](http://www.yingdev.com/projects/wgestures) 开启。
或打包成 .exe 文件后通过 Windows 快捷方式的快捷键启动。

## 开源相关
本项目参考了 [Image2Text](https://github.com/shuoGG1239/Image2Text) 的部分源码
