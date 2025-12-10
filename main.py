import sys

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from PyQt5 import QtWebEngineWidgets
except ImportError as exc:
    raise SystemExit(
        "PyQt5.QtWebEngineWidgets is required. Install PyQt5 with web engine "
        "support (e.g. `pip install PyQt5 PyQtWebEngine`)."
    ) from exc













class BrowserWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NovaBrowse")
        self.resize(1200, 800)


        self.web_view = QtWebEngineWidgets.QWebEngineView()
        self.web_view.setUrl(QtCore.QUrl("https://example.com"))

        self.url_bar = QtWidgets.QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL and press Enter…")
        self.url_bar.returnPressed.connect(self.load_url)

        go_button = QtWidgets.QPushButton("Go")
        go_button.clicked.connect(self.load_url)

        back_button = QtWidgets.QPushButton("Back")
        back_button.clicked.connect(self.web_view.back)

        forward_button = QtWidgets.QPushButton("Forward")
        forward_button.clicked.connect(self.web_view.forward)

        reload_button = QtWidgets.QPushButton("Reload")
        reload_button.clicked.connect(self.web_view.reload)

        nav_layout = QtWidgets.QHBoxLayout()
        nav_layout.addWidget(back_button)
        nav_layout.addWidget(forward_button)
        nav_layout.addWidget(reload_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(go_button)



        central_widget = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central_widget)
        central_layout.addLayout(nav_layout)
        central_layout.addWidget(self.web_view)
        self.setCentralWidget(central_widget)


        self.web_view.urlChanged.connect(self._sync_url_bar)

    def load_url(self) -> None:
        raw_input = self.url_bar.text().strip()
        if not raw_input:
            return
        if "://" not in raw_input:
            raw_input = f"https://{raw_input}"

        url = QtCore.QUrl.fromUserInput(raw_input)
        if not url.isValid():
            self.statusBar().showMessage("Invalid URL. Please try again.", 5000)
            return

        self._set_url_bar_text(url.toString())
        self.web_view.setUrl(url)

    def _sync_url_bar(self, url: QtCore.QUrl) -> None:
        if self.url_bar.hasFocus() and self.url_bar.isModified():
            return
        self._set_url_bar_text(url.toString())

    def _set_url_bar_text(self, text: str) -> None:
        if self.url_bar.text() == text:
            self.url_bar.setModified(False)
            return

        was_blocked = self.url_bar.blockSignals(True)
        try:
            self.url_bar.setText(text)
        finally:
            self.url_bar.blockSignals(was_blocked)
        self.url_bar.setModified(False)







def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
