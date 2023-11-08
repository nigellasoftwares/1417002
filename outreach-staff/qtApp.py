import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from flask import Flask, request, render_template
from threading import Thread

app = Flask(__name__)

def create_webview():
    class WebApp(QMainWindow):
        def __init__(self):
            super().__init__()
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl('http://159.223.32.228:5010/'))
            self.setCentralWidget(self.browser)

    app_instance = QApplication([])
    window = WebApp()
    window.show()
    app_instance.exec_()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Create a separate thread for the webview to avoid conflicts with Flask
    webview_thread = Thread(target=create_webview)
    webview_thread.start()

    app.run()