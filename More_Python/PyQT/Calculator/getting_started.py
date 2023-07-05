import sys

# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import QWidget


def f1():
    # 2. Create an instance of QApplication
    app = QApplication([])

    # 3. Create your application's GUI
    window = QWidget()
    window.setWindowTitle("PyQt App")
    window.setGeometry(0, 100, 600, 600)

    # window.setGeometry(100, 100, 280, 80)

    h1_text = '<h1> h1_element </h1>'
    h1_label = QLabel(text=h1_text, parent=window)

    h2_text = '<h2> h2_element </h2>'
    h2_label = QLabel(text=h2_text, parent=h1_label)

    window.show()

    sys.exit(app.exec())


from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
)


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        self.setCentralWidget(QLabel("I'm the Central Widget"))
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
