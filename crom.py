import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Web Browser')
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://www.google.com'))
        self.setCentralWidget(self.browser)
        self.setMinimumSize(800, 600)

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('←', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('→', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('⟳', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('⌂', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        about_btn = QAction('ℹ', self)
        about_btn.triggered.connect(self.show_about_dialog)
        navbar.addAction(about_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.history_dropdown = QComboBox()
        self.history_dropdown.setFocusPolicy(Qt.NoFocus)
        self.history_dropdown.setMaximumWidth(200)
        navbar.addWidget(self.history_dropdown)

        self.load_history()
        self.update_history_dropdown()
        self.history_dropdown.currentIndexChanged.connect(self.history_item_selected)

        navbar.setStyleSheet("""
            QToolBar {
                spacing: 10px;
                background-color: #f0f0f0;
                border: none;
                padding: 5px;
            }
            QToolBar QToolButton {
                border: none;
                padding: 5px;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

    def navigate_home(self):
        self.browser.setUrl(QUrl('http://www.google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.navigate(url)

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def navigate(self, url):
        if not url.startswith(("http://", "https://")):
            url = "http://" + url if not url.startswith("www.") else "http://" + url
            self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))
        self.add_to_history(url)

    def load_history(self):
        try:
            with open('history.json', 'r') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def save_history(self):
        with open('history.json', 'w') as f:
            json.dump(self.history, f)

    def add_to_history(self, url):
        if url not in self.history:
            self.history.insert(0, url)
            self.save_history()
            self.update_history_dropdown()

    def update_history_dropdown(self):
        self.history_dropdown.clear()
        self.history_dropdown.addItems(self.history)

    def history_item_selected(self, index):
        url = self.history_dropdown.itemText(index)
        self.navigate(url)

    def show_about_dialog(self):
        about_text = """
        <h2>About crom</h2>
        <p>Imade a web browser</p>
        <p>Author: stratosvomvos</p>
        <p>Version: 0.6969696969696969679699669</p>
        """
        QMessageBox.about(self, "About", about_text)

    def closeEvent(self, event):
        self.save_history()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
