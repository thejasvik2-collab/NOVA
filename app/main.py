import sys
import sqlite3
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
client = genai.Client()
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "nova.db")

def save_message(role, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    cursor.execute(
        "INSERT INTO chat_history (role, message) VALUES (?, ?)",
        (role, message)
    )
    conn.commit()
    conn.close()

def load_messages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    cursor.execute(
        "SELECT role, message FROM chat_history ORDER BY id"
    )
    messages = cursor.fetchall()
    conn.commit()
    conn.close()
    return messages
import psutil
conversation_history = []
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QWidget,
    QFrame,
    QStackedWidget,
    QLineEdit,
    QComboBox,
    QScrollArea,

)

from app.database.database import (
    initialize_database,
    add_task,
    get_tasks,
    complete_task,
    delete_task,
    initialize_notes_table,
    add_note,
    get_notes,
    delete_note,

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





class TaskWidget(QFrame):

    def __init__(self, task, refresh_callback):

        super().__init__()



        self.task_id = task[0]

        title = task[1]

        completed = task[2]

        priority = task[3]



        self.setObjectName("taskItem")



        layout = QHBoxLayout(self)

        layout.setContentsMargins(15, 10, 15, 10)



        # Complete button

        complete_button = QPushButton("✓" if completed else "○")

        complete_button.setObjectName("completeButton")

        complete_button.setFixedWidth(40)



        if not completed:

            complete_button.clicked.connect(self.complete)



        layout.addWidget(complete_button)



        # Task title

        title_label = QLabel(title)

        title_label.setObjectName("taskTitle")



        if completed:

            title_label.setProperty("completed", True)



        layout.addWidget(title_label)



        # Priority

        priority_label = QLabel(priority)

        priority_label.setObjectName("priority")



        layout.addWidget(priority_label)



        # Delete

        delete_button = QPushButton("×")

        delete_button.setObjectName("deleteButton")

        delete_button.setFixedWidth(35)



        delete_button.clicked.connect(self.delete)



        layout.addWidget(delete_button)



    def complete(self):

        complete_task(self.task_id)

        self.refresh()



    def delete(self):

        delete_task(self.task_id)

        self.refresh()



    def refresh(self):

        parent = self.parentWidget()



        while parent and not hasattr(parent, "load_tasks"):

            parent = parent.parentWidget()



        if parent:

            parent.load_tasks()





class NovaWindow(QMainWindow):



    def __init__(self):

        super().__init__()



        self.setWindowTitle("NOVA")

        self.resize(1100, 700)



        initialize_database()

        initialize_notes_table()



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



        self.pages.addWidget(self.create_dashboard_page())



        self.pages.addWidget(self.create_assistant_page())
        
        



        self.pages.addWidget(self.create_tasks_page())
     


        self.pages.addWidget(

            self.create_notes_page()



            )





        self.pages.addWidget(

            self.create_placeholder_page(

                "⏱ Focus",

                "Stay focused with a Pomodoro timer."

            )

        )



        self.pages.addWidget(

            self.create_placeholder_page(

                "📊 Analytics",

                "View your productivity statistics."

            )

        )



        self.pages.addWidget(

            self.create_placeholder_page(

                "🖥 PC Monitor",

                "Detailed information about your computer."

            )

        )



        self.pages.addWidget(

            self.create_placeholder_page(

                "⚙ Settings",

                "Customize NOVA."

            )

        )



        main_layout.addWidget(sidebar)

        main_layout.addWidget(self.pages)



        self.change_page(0)



        # =========================

        # SYSTEM TIMER

        # =========================



        self.timer = QTimer()

        self.timer.timeout.connect(self.update_stats)

        self.timer.start(1000)



        self.update_stats()



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

            }



            #placeholderTitle {

                font-size: 30px;

                font-weight: bold;

            }



            #placeholderDescription {

                color: #888894;

                font-size: 15px;

            }



            #taskInput {

                background-color: #161620;

                border: 1px solid #30303d;

                border-radius: 10px;

                padding: 12px;

                color: white;

                font-size: 14px;

            }



            #priorityBox {

                background-color: #161620;

                border: 1px solid #30303d;

                border-radius: 10px;

                padding: 10px;

            }



            #addButton {

                background-color: #292943;

                border: none;

                border-radius: 10px;

                padding: 12px 20px;

                font-weight: bold;

            }



            #addButton:hover {

                background-color: #393957;

            }



            #taskItem {

                background-color: #161620;

                border: 1px solid #282835;

                border-radius: 10px;

                margin-bottom: 6px;

            }



            #completeButton,

            #deleteButton {

                background-color: transparent;

                border: none;

                font-size: 18px;

            }



            #taskTitle {

                font-size: 14px;

            }



            #taskTitle[completed="true"] {

                color: #777784;

            }



            #priority {

                color: #9999a8;

                font-size: 12px;

            }

        """)



    # =========================

    # DASHBOARD

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

    # TASKS PAGE

    # =========================



    def create_tasks_page(self):



        page = QWidget()



        layout = QVBoxLayout(page)

        layout.setContentsMargins(35, 30, 35, 30)



        title = QLabel("Tasks")

        title.setObjectName("title")



        description = QLabel(

            "Organize what you need to get done."

        )

        description.setObjectName("description")



        layout.addWidget(title)

        layout.addWidget(description)

        layout.addSpacing(20)



        # Add task area

        input_layout = QHBoxLayout()



        self.task_input = QLineEdit()

        self.task_input.setObjectName("taskInput")

        self.task_input.setPlaceholderText("Add a new task...")



        self.priority_box = QComboBox()

        self.priority_box.setObjectName("priorityBox")



        self.priority_box.addItems([

            "Low",

            "Medium",

            "High"

        ])



        add_button = QPushButton("+ Add")

        add_button.setObjectName("addButton")

        add_button.setCursor(Qt.PointingHandCursor)



        add_button.clicked.connect(self.add_new_task)



        self.task_input.returnPressed.connect(

            self.add_new_task

        )



        input_layout.addWidget(self.task_input)

        input_layout.addWidget(self.priority_box)

        input_layout.addWidget(add_button)



        layout.addLayout(input_layout)

        layout.addSpacing(20)



        self.task_scroll = QScrollArea()

        self.task_scroll.setWidgetResizable(True)

        self.task_scroll.setFrameShape(QFrame.NoFrame)



        self.task_container = QWidget()



        self.task_layout = QVBoxLayout(

            self.task_container

        )



        self.task_layout.setAlignment(Qt.AlignTop)



        self.task_scroll.setWidget(

            self.task_container

        )



        layout.addWidget(self.task_scroll)



        self.load_tasks()



        return page



    # =========================

    # LOAD TASKS

    # =========================



    def load_tasks(self):



        # Remove old widgets

        while self.task_layout.count():



            item = self.task_layout.takeAt(0)



            widget = item.widget()



            if widget:

                widget.deleteLater()



        tasks = get_tasks()



        if not tasks:



            empty = QLabel(

                "No tasks yet. Add your first task above!"

            )



            empty.setObjectName("description")



            self.task_layout.addWidget(empty)



            return



        for task in tasks:



            widget = TaskWidget(

                task,

                self.load_tasks

            )



            self.task_layout.addWidget(widget)



    # =========================

    # ADD TASK

    # =========================



    def add_new_task(self):



        title = self.task_input.text().strip()



        if not title:

            return



        priority = self.priority_box.currentText()



        add_task(

            title,

            priority

        )



        self.task_input.clear()



        self.load_tasks()
# =========================
# ASSISTANT PAGE
# =========================
    def create_assistant_page(self):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(15)

        title = QLabel("🤖 AI Assistant")
        title.setObjectName("title")

        description = QLabel("Your intelligent desktop assistant.")
        description.setObjectName("description")

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addSpacing(10)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setPlaceholderText("NOVA's responses will appear here...")
        self.chat_area.setObjectName("chatArea")

        layout.addWidget(self.chat_area, 1)

        input_layout = QHBoxLayout()

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask NOVA something...")
        self.chat_input.setObjectName("chatInput")

        send_button = QPushButton("➤ Send")
        send_button.setObjectName("primaryButton")

        send_button.clicked.connect(self.send_message)
        self.chat_input.returnPressed.connect(self.send_message)

        input_layout.addWidget(self.chat_input, 1)
        input_layout.addWidget(send_button)

        layout.addLayout(input_layout)

        return page


    def send_message(self):
        message = self.chat_input.text().strip()
        if not message:
            return
        self.chat_area.append(f"<b>You:</b> {message}")
        self.chat_input.clear()
        conversation_history.append(f"User: {message}")
        save_message("user", message)
        try:
            prompt = "\n".join(conversation_history)
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=f"""You are NOVA, a helpful desktop AI assistant.
    Keep your answers clear, useful, and reasonably concise.
    Conversation:
    {prompt}
    NOVA:"""
            )
            reply = response.text
            conversation_history.append(f"NOVA: {reply}")
            save_message("nova", reply)
            self.chat_area.append(f"<b>NOVA:</b> {reply}")
        except Exception as e:
            self.chat_area.append(f"<b>NOVA:</b> API error: {e}")
        # NOTES PAGE

    # =========================



    def create_notes_page(self):



        page = QWidget()



        layout = QVBoxLayout(page)

        layout.setContentsMargins(35, 30, 35, 30)



        title = QLabel("Notes")

        title.setObjectName("title")



        description = QLabel(

            "Write down ideas, information and things you want to remember."

        )

        description.setObjectName("description")



        layout.addWidget(title)

        layout.addWidget(description)

        layout.addSpacing(20)



        self.note_title = QLineEdit()

        self.note_title.setObjectName("taskInput")

        self.note_title.setPlaceholderText("Note title...")



        layout.addWidget(self.note_title)



        self.note_content = QLineEdit()

        self.note_content.setObjectName("taskInput")

        self.note_content.setPlaceholderText("Write your note...")



        layout.addWidget(self.note_content)



        save_button = QPushButton("💾 Save Note")

        save_button.setObjectName("addButton")

        save_button.setCursor(Qt.PointingHandCursor)



        save_button.clicked.connect(self.save_note)



        layout.addWidget(save_button)



        layout.addSpacing(25)



        notes_title = QLabel("Saved notes")

        notes_title.setObjectName("sectionTitle")



        layout.addWidget(notes_title)



        self.notes_scroll = QScrollArea()

        self.notes_scroll.setWidgetResizable(True)

        self.notes_scroll.setFrameShape(QFrame.NoFrame)



        self.notes_container = QWidget()



        self.notes_layout = QVBoxLayout(

            self.notes_container

        )



        self.notes_layout.setAlignment(Qt.AlignTop)



        self.notes_scroll.setWidget(

            self.notes_container

        )



        layout.addWidget(self.notes_scroll)



        self.load_notes()



        return page





    def save_note(self):



        title = self.note_title.text().strip()

        content = self.note_content.text().strip()



        if not title or not content:

            return



        add_note(title, content)



        self.note_title.clear()

        self.note_content.clear()



        self.load_notes()





    def load_notes(self):



        while self.notes_layout.count():



            item = self.notes_layout.takeAt(0)



            widget = item.widget()



            if widget:

                widget.deleteLater()



        notes = get_notes()



        if not notes:



            empty = QLabel(

                "No notes yet. Create your first note above!"

            )



            empty.setObjectName("description")



            self.notes_layout.addWidget(empty)



            return



        for note in notes:



            note_id = note[0]

            title = note[1]

            content = note[2]



            card = QFrame()

            card.setObjectName("taskItem")



            card_layout = QHBoxLayout(card)



            text_layout = QVBoxLayout()



            note_title = QLabel(title)

            note_title.setObjectName("sectionTitle")



            note_content = QLabel(content)

            note_content.setObjectName("description")

            note_content.setWordWrap(True)



            text_layout.addWidget(note_title)

            text_layout.addWidget(note_content)



            delete_button = QPushButton("×")

            delete_button.setObjectName("deleteButton")

            delete_button.setFixedWidth(35)



            delete_button.clicked.connect(

                lambda checked=False, note_id=note_id:

                self.remove_note(note_id)

            )



            card_layout.addLayout(text_layout)

            card_layout.addWidget(delete_button)



            self.notes_layout.addWidget(card)





    def remove_note(self, note_id):



        delete_note(note_id)



        self.load_notes()

    # =========================

    # PLACEHOLDER

    # =========================



    def create_placeholder_page(

        self,

        title_text,

        description_text

    ):



        page = QWidget()



        layout = QVBoxLayout(page)



        layout.setContentsMargins(

            50,

            45,

            50,

            45

        )



        title = QLabel(title_text)

        title.setObjectName(

            "placeholderTitle"

        )



        description = QLabel(

            description_text

        )



        description.setObjectName(

            "placeholderDescription"

        )



        layout.addWidget(title)

        layout.addWidget(description)



        layout.addStretch()



        return page



    # =========================

    # NAVIGATION

    # =========================



    def change_page(self, index):



        self.pages.setCurrentIndex(index)



        for i, button in enumerate(

            self.nav_buttons

        ):



            button.setProperty(

                "active",

                i == index

            )



            button.style().unpolish(

                button

            )



            button.style().polish(

                button

            )



    # =========================

    # SYSTEM MONITOR

    # =========================



    def update_stats(self):



        cpu = psutil.cpu_percent()



        memory = psutil.virtual_memory().percent



        disk = psutil.disk_usage("/").percent



        self.cpu_card.value.setText(

            f"{cpu:.0f}%"

        )



        self.memory_card.value.setText(

            f"{memory:.0f}%"

        )



        self.disk_card.value.setText(

            f"{disk:.0f}%"

        )



        self.system_info.setText(

            f"CPU usage: {cpu:.1f}%    •    "

            f"Memory usage: {memory:.1f}%    •    "

            f"Disk usage: {disk:.1f}%"

        )





def main():



    app = QApplication(sys.argv)



    window = NovaWindow()



    window.show()



    sys.exit(

        app.exec()

    )





if __name__ == "__main__":

    main()
