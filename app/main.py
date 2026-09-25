import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtCore import Qt


class NovaWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NOVA")
        self.resize(1100, 700)

        label = QLabel("NOVA")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)


def main():
    app = QApplication(sys.argv)

    window = NovaWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()