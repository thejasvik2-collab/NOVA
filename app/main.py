import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)


class NovaWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NOVA")
        self.resize(1100, 700)

        # Main container
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =========================
        # SIDEBAR
        # =========================

        sidebar = QWidget()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 25, 20, 25)
        sidebar_layout.setSpacing(10)

        # Logo
        logo = QLabel("NOVA")
        logo.setObjectName("logo")

        subtitle = QLabel("Your personal command center")
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(subtitle)
        sidebar_layout.addSpacing(30)

        # Navigation buttons
        buttons = [
            "🏠  Dashboard",
            "🤖  Assistant",
            "✅  Tasks",
            "📝  Notes",
            "⏱  Focus",
            "📊  Analytics",
            "🖥  PC Monitor",
        ]

        for text in buttons:
            button = QPushButton(text)
            button.setObjectName("navButton")
            button.setCursor(Qt.PointingHandCursor)

            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        settings = QPushButton("⚙  Settings")
        settings.setObjectName("navButton")
        sidebar_layout.addWidget(settings)

        # =========================
        # CONTENT AREA
        # =========================

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(35, 30, 35, 30)

        title = QLabel("Good afternoon 👋")
        title.setObjectName("title")

        description = QLabel(
            "Welcome to NOVA. Your personal productivity command center."
        )
        description.setObjectName("description")

        content_layout.addWidget(title)
        content_layout.addWidget(description)

        content_layout.addStretch()

        # Add sidebar + content
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        # =========================
        # STYLE
        # =========================

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d0d14;
            }

            QWidget {
                background-color: #0d0d14;
                color: #f5f5f7;
                font-family: "Segoe UI";
            }

            #logo {
                font-size: 30px;
                font-weight: bold;
            }

            #subtitle {
                color: #888894;
                font-size: 12px;
            }

            #navButton {
                background-color: transparent;
                border: none;
                border-radius: 10px;
                padding: 12px;
                text-align: left;
                font-size: 14px;
                color: #b9b9c5;
            }

            #navButton:hover {
                background-color: #1c1c27;
                color: white;
            }

            #title {
                font-size: 30px;
                font-weight: bold;
            }

            #description {
                color: #888894;
                font-size: 14px;
            }
        """)


def main():
    app = QApplication(sys.argv)

    window = NovaWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()