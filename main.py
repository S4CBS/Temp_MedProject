import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QSpacerItem, QSizePolicy, QLabel, 
                               QLineEdit, QStackedWidget, QFormLayout, QDateTimeEdit, QTimeEdit, QComboBox, QListWidget, QListWidgetItem, QTextEdit, QPlainTextEdit)
from PySide6.QtGui import QPalette, QColor, QIcon, QFont, QKeyEvent
from PySide6.QtCore import Qt, QTimer, QDateTime, QTime

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.reminders = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MedProject")

        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        self.setFixedSize(screen_width * 0.8, screen_height * 0.8)

        self.stacked_widget = QStackedWidget()
        
        self.main_widget = QWidget()
        self.init_main_page()
        
        self.doctor_login_widget = QWidget()
        self.init_doctor_login_page()
        
        self.doctor_main_widget = QWidget()
        self.init_doctor_main_page()

        self.patient_login_widget = QWidget()
        self.init_patient_login_page()

        self.patient_main_widget = QWidget()
        self.init_patient_main_page()
        
        self.reminder_widget = QWidget()
        self.init_reminder_page()

        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.doctor_login_widget)
        self.stacked_widget.addWidget(self.doctor_main_widget)
        self.stacked_widget.addWidget(self.patient_login_widget)
        self.stacked_widget.addWidget(self.patient_main_widget)
        self.stacked_widget.addWidget(self.reminder_widget)
        
        self.stacked_widget.setCurrentWidget(self.main_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        self.apply_theme()

    def init_main_page(self):
        main_layout = QVBoxLayout(self.main_widget)

        center_layout = QVBoxLayout()
        center_layout.addStretch()

        button_font = QFont("Arial", 16)

        doctor_button = QPushButton("для Врача", self.main_widget)
        doctor_button.setFont(button_font)
        doctor_button.setFixedSize(200, 100)
        doctor_button.setStyleSheet(self.button_stylesheet())
        doctor_button.clicked.connect(self.open_doctor_interface)
        center_layout.addWidget(doctor_button)

        patient_button = QPushButton("для Пациента", self.main_widget)
        patient_button.setFont(button_font)
        patient_button.setFixedSize(200, 100)
        patient_button.setStyleSheet(self.button_stylesheet())
        patient_button.clicked.connect(self.open_patient_interface)
        center_layout.addWidget(patient_button)

        center_layout.addStretch()

        inner_layout = QHBoxLayout()
        inner_layout.addStretch()
        inner_layout.addLayout(center_layout)
        inner_layout.addStretch()

        main_layout.addLayout(inner_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.theme_button = QPushButton(self.main_widget)
        self.theme_button.setObjectName("themeButton")
        script_dir = os.path.dirname(sys.argv[0])
        icon_path = os.path.join(script_dir, 'images', 'image1.png')
        self.theme_button.setIcon(QIcon(icon_path))
        self.theme_button.setIconSize(self.theme_button.sizeHint())
        self.theme_button.clicked.connect(self.switch_theme)
        self.theme_button.setStyleSheet("background: transparent; border: none;")
        bottom_layout.addWidget(self.theme_button)
        main_layout.addLayout(bottom_layout)

        self.main_widget.setLayout(main_layout)

    def init_navigation_buttons(self, parent_widget):
        # Кнопка для перехода на предыдущую страницу
        prev_button = QPushButton("Предыдущая", parent_widget)
        prev_button.clicked.connect(self.go_to_previous_page)

        # Кнопка для перехода на следующую страницу
        next_button = QPushButton("Следующая", parent_widget)
        next_button.clicked.connect(self.go_to_next_page)

        # Горизонтальный лэйаут для размещения кнопок
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(next_button)

        return nav_layout

    def go_to_previous_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 2)

    def go_to_next_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)


    def init_doctor_login_page(self):
        login_layout = QVBoxLayout(self.doctor_login_widget)
        
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        
        login_button = QPushButton("Login", self.doctor_login_widget)
        login_button.setFixedSize(200, 50)
        login_button.setStyleSheet(self.button_stylesheet())
        login_button.clicked.connect(self.verify_doctor_credentials)

        # Кнопка "Назад"
        back_button = QPushButton("Назад", self.doctor_login_widget)
        back_button.setFixedSize(200, 50)
        back_button.setStyleSheet(self.button_stylesheet())
        back_button.clicked.connect(self.go_back_to_main_page)
        
        login_layout.addStretch()
        login_layout.addLayout(form_layout)
        login_layout.addWidget(login_button)
        login_layout.addWidget(back_button)
        login_layout.addStretch()

    def go_back_to_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_widget)
        
    def init_doctor_main_page(self):
        layout = QVBoxLayout(self.doctor_main_widget)

        prescribe_med_button = QPushButton("Выписать лекарства", self.doctor_main_widget)
        prescribe_med_button.setFont(QFont("Arial", 16))
        prescribe_med_button.setStyleSheet(self.button_stylesheet())
        prescribe_med_button.clicked.connect(self.prescribe_medication)
        layout.addWidget(prescribe_med_button)

        layout.addStretch()
        layout.setAlignment(Qt.AlignHCenter)

        # Кнопка "Назад"
        back_button = QPushButton("Назад", self.doctor_main_widget)
        back_button.setFont(QFont("Arial", 16))
        back_button.setStyleSheet(self.button_stylesheet())
        back_button.clicked.connect(self.go_back_to_main_page)
        layout.addWidget(back_button)

        self.init_theme_button(self.doctor_main_widget)
        
        # Добавляем кнопку "Назад" в layout
        layout.addWidget(back_button)

        # Добавляем layout к виджету
        self.doctor_main_widget.setLayout(layout)


    def prescribe_medication(self):
        print("Prescribing medication...")

    def switch_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def button_stylesheet(self):
        if self.current_theme == "light":
            return """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #000000;
                border-radius: 10px;
            }
            QPushButton#themeButton {
                background: transparent; 
                border: none; /* Removing border from theme change button */
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            """
        else:
            return """
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: 2px solid #ffffff;
                border-radius: 10px;
            }
            QPushButton#themeButton {
                background: transparent; 
                border: none; /* Removing border from theme change button */
            }
            QPushButton:hover {
                background-color: #555555;
            }
            """

    def open_doctor_interface(self):
        self.stacked_widget.setCurrentWidget(self.doctor_login_widget)

    def verify_doctor_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":
            self.stacked_widget.setCurrentWidget(self.doctor_main_widget)
        else:
            print("Incorrect username or password")

    def open_patient_interface(self):
        self.stacked_widget.setCurrentWidget(self.patient_login_widget)

    
    def init_patient_login_page(self):
        self.patient_login_widget = QWidget()  # Создаем виджет для страницы входа пациента

        # Вертикальный лэйаут для страницы входа пациента
        login_layout = QVBoxLayout(self.patient_login_widget)
        login_layout.setAlignment(Qt.AlignCenter)

        # Вертикальный лэйаут для элементов ввода
        form_layout = QFormLayout()
        self.patient_username_input = QLineEdit()
        self.patient_password_input = QLineEdit()
        self.patient_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Username:", self.patient_username_input)
        form_layout.addRow("Password:", self.patient_password_input)

        # Добавляем вертикальный лэйаут с элементами ввода в общий вертикальный лэйаут
        login_layout.addLayout(form_layout)

        login_button = QPushButton("Login", self.patient_login_widget)
        login_button.setFixedSize(200, 50)
        login_button.setStyleSheet(self.button_stylesheet())
        login_button.clicked.connect(self.verify_patient_credentials)

        login_layout.addWidget(login_button)

        # Кнопка "Назад"
        back_button = QPushButton("Назад", self.patient_login_widget)
        back_button.setFixedSize(login_button.size())  # Устанавливаем размер кнопки "Назад" таким же, как у кнопки "Login"
        back_button.setStyleSheet(self.button_stylesheet())
        back_button.clicked.connect(self.go_back_to_main_page)
        login_layout.addWidget(back_button)

        login_layout.addStretch()


    def verify_patient_credentials(self):
        username = self.patient_username_input.text()
        password = self.patient_password_input.text()

        # Простейшая проверка логина и пароля (замените на свою логику проверки)
        if username == "patient" and password == "patient":
            self.stacked_widget.setCurrentWidget(self.patient_main_widget)
        else:
            print("Неверный логин или пароль для пациента")

    def init_patient_main_page(self):
        layout = QVBoxLayout(self.patient_main_widget)

        med_form_layout = QFormLayout()
        
        self.med_name_input = QLineEdit()
        med_form_layout.addRow("Название лекарства:", self.med_name_input)
        
        self.start_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_date_input.setCalendarPopup(True)
        med_form_layout.addRow("Дата начала:", self.start_date_input)
        
        self.end_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.end_date_input.setCalendarPopup(True)
        med_form_layout.addRow("Дата окончания:", self.end_date_input)
        
        self.dosage_input = QLineEdit()
        med_form_layout.addRow("Дозировка (г):", self.dosage_input)
        
        self.times_per_day_input = QComboBox()
        self.times_per_day_input.addItems([str(i) for i in range(0, 5)])
        med_form_layout.addRow("Приемов в день:", self.times_per_day_input)

        self.times_inputs = []
        for _ in range(4):
            time_input = QTimeEdit()
            time_input.hide()
            self.times_inputs.append(time_input)
            med_form_layout.addRow("Время приема:", time_input)
        
        self.times_per_day_input.currentTextChanged.connect(self.update_time_inputs)

        save_button = QPushButton("Сохранить", self.patient_main_widget)
        save_button.setFont(QFont("Arial", 16))
        save_button.setStyleSheet(self.button_stylesheet())
        save_button.clicked.connect(self.save_medication)
        layout.addLayout(med_form_layout)
        layout.addWidget(save_button)

        layout.addStretch()
        layout.setAlignment(Qt.AlignHCenter)

        # Кнопка смены темы
        self.init_theme_button(self.patient_main_widget)
        layout.addWidget(self.theme_button)

        # Кнопка "Назад"
        back_button = QPushButton("Назад", self.patient_main_widget)
        back_button.setFont(QFont("Arial", 16))
        back_button.setStyleSheet(self.button_stylesheet())
        back_button.clicked.connect(self.go_back_to_main_page)
        layout.addWidget(back_button)

        self.patient_main_widget.setLayout(layout)

    def update_time_inputs(self, count):
        for i, time_input in enumerate(self.times_inputs):
            if i < int(count):
                time_input.show()
            else:
                time_input.hide()

    def save_medication(self):
        med_name = self.med_name_input.text()
        start_date = self.start_date_input.dateTime().toString()
        end_date = self.end_date_input.dateTime().toString()
        dosage = self.dosage_input.text()
        times_per_day = int(self.times_per_day_input.currentText())
        times = [self.times_inputs[i].time().toString() for i in range(times_per_day)]

        print(f"Medication saved: {med_name}, from {start_date} to {end_date}, {dosage}g, {times_per_day} times per day at {', '.join(times)}")

        self.reminders.append((med_name, times))
        self.set_reminders(med_name, times)

        self.update_reminder_list()

    def set_reminders(self, med_name, times):
        for time in times:
            timer = QTimer(self)
            timer.timeout.connect(lambda: self.show_reminder(med_name))
            now = QDateTime.currentDateTime()
            target_time = QDateTime(now.date(), QTime.fromString(time, "hh:mm:ss"))
            interval = target_time.toMSecsSinceEpoch() - now.toMSecsSinceEpoch()
            if interval < 0:
                interval += 86400000  # Добавляем 24 часа в миллисекундах, если время прошло
            timer.start(interval)

    def show_reminder(self, med_name):
        reminder = QWidget()
        reminder.setWindowTitle("Напоминание")
        layout = QVBoxLayout()
        label = QLabel(f"Пора принять лекарство: {med_name}")
        layout.addWidget(label)
        reminder.setLayout(layout)
        reminder.show()
        QTimer.singleShot(10000, reminder.close)  # Закрыть напоминание через 10 секунд

    def init_theme_button(self, parent_widget):
        self.theme_button = QPushButton(parent_widget)
        self.theme_button.setObjectName("themeButton")
        script_dir = os.path.dirname(sys.argv[0])
        icon_path = os.path.join(script_dir, 'images', 'image1.png')
        self.theme_button.setIcon(QIcon(icon_path))
        self.theme_button.setIconSize(self.theme_button.sizeHint())
        self.theme_button.clicked.connect(self.switch_theme)
        self.theme_button.setStyleSheet("background: transparent; border: none;")

    def apply_theme(self):
        palette = QPalette()
        if self.current_theme == "light":
            palette.setColor(QPalette.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(242, 242, 242))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
            palette.setColor(QPalette.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.Button, QColor(255, 255, 255))
            palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Highlight, QColor(38, 79, 120))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        else:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.Base, QColor(42, 42, 42))
            palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
            palette.setColor(QPalette.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Highlight, QColor(142, 45, 197))
            palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

        self.setPalette(palette)

        # Set text color for input fields to always be black
        input_field_palette = QPalette()
        input_field_palette.setColor(QPalette.Text, QColor(0, 0, 0))  # Text color is black

        # Apply the input field palette to all relevant input widgets
        input_widgets = (
            self.findChildren(QLineEdit) +
            self.findChildren(QTextEdit) +
            self.findChildren(QPlainTextEdit) +
            self.findChildren(QDateTimeEdit) +
            self.findChildren(QComboBox)
        )

        for input_widget in input_widgets:
            input_widget.setPalette(input_field_palette)

    def init_reminder_page(self):
        layout = QVBoxLayout(self.reminder_widget)
        self.reminder_list = QListWidget()
        layout.addWidget(self.reminder_list)

        back_button = QPushButton("Назад", self.reminder_widget)
        back_button.setFixedSize(200, 50)
        back_button.setStyleSheet(self.button_stylesheet())
        back_button.clicked.connect(self.go_back_to_patient_main)
        layout.addWidget(back_button)

        nav_layout = self.init_navigation_buttons(self.reminder_widget)
        layout.addLayout(nav_layout)

    def go_back_to_patient_main(self):
        self.stacked_widget.setCurrentWidget(self.patient_main_widget)

    def update_reminder_list(self):
        self.reminder_list.clear()
        for med_name, times in self.reminders:
            for time in times:
                item = QListWidgetItem(f"{med_name} - {time}")
                self.reminder_list.addItem(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.stacked_widget.setCurrentIndex((self.stacked_widget.currentIndex() + 1) % self.stacked_widget.count())
        elif event.key() == Qt.Key_Left:
            self.stacked_widget.setCurrentIndex((self.stacked_widget.currentIndex() - 1) % self.stacked_widget.count())

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
