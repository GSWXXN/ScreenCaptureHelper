if __name__ == '__main__':
    from PyInstaller.__main__ import run

    opts = ['main.py',
            '-F',
            '-w',
            '-n=屏幕捕捉助手',
            '--hidden-import=queue',
            '--icon=./asset/favicon.ico',
            '--version-file=./version.txt',
            '--add-binary=./asset/icon.ico;asset',
            '--add-binary=./asset/screenshot.ico;asset',
            '--upx-dir=./upx'
            ]
    run(opts)
