import sys
import psutil

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFrame,
    QStackedWidget,
)


class StatCard(QFrame):
    def __init__(self, title):
        super().__init__()

        self.setObjectName("statCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)

        self.title = QLabel(title)
        self.title.setObjectName("cardTitle")

        self.value = QLabel("0%")
        self.value.setObjectName("cardValue")

        self.status = QLabel("● Normal")
        self.status.setObjectName("cardStatus")

        layout.addWidget(self.title)
        layout.addWidget(self.value)
        layout.addWidget(self.status)


class NovaWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NOVA")
        self.resize(1100, 700)

        # =========================
        # MAIN WINDOW
        # =========================

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =========================
        # SIDEBAR
        # =========================

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 25, 20, 25)
        sidebar_layout.setSpacing(8)

        logo = QLabel("NOVA")
        logo.setObjectName("logo")

        subtitle = QLabel("Your personal command center")
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(subtitle)
        sidebar_layout.addSpacing(30)

        # Navigation buttons
        navigation = [
            ("🏠  Dashboard", 0),
            ("🤖  Assistant", 1),
            ("✅  Tasks", 2),
            ("📝  Notes", 3),
            ("⏱  Focus", 4),
            ("📊  Analytics", 5),
            ("🖥  PC Monitor", 6),
        ]

        self.nav_buttons = []

        for text, page_index in navigation:

            button = QPushButton(text)

            button.setObjectName("navButton")
            button.setCursor(Qt.PointingHandCursor)

            button.clicked.connect(
                lambda checked=False, index=page_index:
                self.change_page(index)
            )

            self.nav_buttons.append(button)
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        settings = QPushButton("⚙  Settings")
        settings.setObjectName("navButton")
        settings.setCursor(Qt.PointingHandCursor)

        settings.clicked.connect(
            lambda: self.change_page(7)
        )

        sidebar_layout.addWidget(settings)

        self.nav_buttons.append(settings)

        # =========================
        # PAGE STACK
        # =========================

        self.pages = QStackedWidget()

        # Create pages
        self.pages.addWidget(self.create_dashboard_page())
        self.pages.addWidget(self.create_placeholder_page(
            "🤖 AI Assistant",
            "Your intelligent desktop assistant."
        ))

        self.pages.addWidget(self.create_placeholder_page(
            "✅ Tasks",
            "Manage your tasks and daily goals."
        ))

        self.pages.addWidget(self.create_placeholder_page(
            "📝 Notes",
            "Create and organize your notes."
        ))

        self.pages.addWidget(self.create_placeholder_page(
            "⏱ Focus",
            "Stay focused with a Pomodoro timer."
        ))

        self.pages.addWidget(self.create_placeholder_page(
            "📊 Analytics",
            "View your productivity statistics."
        ))

        self.pages.addWidget(self.create_placeholder_page(
            "🖥 PC Monitor",
            "Detailed information about your computer."
        ))

        self.pages.addWidget(self.create_placeholder_page(
            "⚙ Settings",
            "Customize NOVA."
        ))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

        # Dashboard is active initially
        self.change_page(0)

        # =========================
        # SYSTEM UPDATE TIMER
        # =========================

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

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

            #sidebar {
                background-color: #11111a;
                border-right: 1px solid #242430;
            }

            #logo {
                font-size: 30px;
                font-weight: bold;
            }

            #subtitle {
                color: #777784;
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
                background-color: #20202c;
                color: white;
            }

            #navButton[active="true"] {
                background-color: #292943;
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

            #statCard {
                background-color: #161620;
                border: 1px solid #282835;
                border-radius: 14px;
            }

            #cardTitle {
                color: #858592;
                font-size: 12px;
                font-weight: bold;
            }

            #cardValue {
                font-size: 32px;
                font-weight: bold;
            }

            #cardStatus {
                color: #6fd18a;
                font-size: 12px;
            }

            #sectionTitle {
                font-size: 18px;
                font-weight: bold;
            }

            #systemInfo {
                color: #8e8e9b;
                font-size: 13px;
                padding-top: 5px;
            }

            #placeholderTitle {
                font-size: 30px;
                font-weight: bold;
            }

            #placeholderDescription {
                color: #888894;
                font-size: 15px;
            }
        """)

    # =========================
    # DASHBOARD PAGE
    # =========================

    def create_dashboard_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(10)

        title = QLabel("Good afternoon 👋")
        title.setObjectName("title")

        description = QLabel(
            "Here's what's happening on your PC."
        )
        description.setObjectName("description")

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(25)

        # Cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        self.cpu_card = StatCard("CPU")
        self.memory_card = StatCard("MEMORY")
        self.disk_card = StatCard("DISK")

        cards_layout.addWidget(self.cpu_card)
        cards_layout.addWidget(self.memory_card)
        cards_layout.addWidget(self.disk_card)

        layout.addLayout(cards_layout)
        layout.addSpacing(25)

        system_title = QLabel("System information")
        system_title.setObjectName("sectionTitle")

        self.system_info = QLabel()
        self.system_info.setObjectName("systemInfo")

        layout.addWidget(system_title)
        layout.addWidget(self.system_info)

        layout.addStretch()

        return page

    # =========================
    # PLACEHOLDER PAGES
    # =========================

    def create_placeholder_page(self, title_text, description_text):

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(50, 45, 50, 45)

        title = QLabel(title_text)
        title.setObjectName("placeholderTitle")

        description = QLabel(description_text)
        description.setObjectName("placeholderDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addStretch()

        return page

    # =========================
    # NAVIGATION
    # =========================

    def change_page(self, index):

        self.pages.setCurrentIndex(index)

        for i, button in enumerate(self.nav_buttons):

            if i == index:
                button.setProperty("active", True)
            else:
                button.setProperty("active", False)

            button.style().unpolish(button)
            button.style().polish(button)

    # =========================
    # SYSTEM MONITORING
    # =========================

    def update_stats(self):

        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        self.cpu_card.value.setText(f"{cpu:.0f}%")
        self.memory_card.value.setText(f"{memory:.0f}%")
        self.disk_card.value.setText(f"{disk:.0f}%")

        self.system_info.setText(
            f"CPU usage: {cpu:.1f}%    •    "
            f"Memory usage: {memory:.1f}%    •    "
            f"Disk usage: {disk:.1f}%"
        )


def main():

    app = QApplication(sys.argv)

    window = NovaWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()