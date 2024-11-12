import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QSize
import sqlite3
from main_menu import MainMenu


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login')
        self.setFixedSize(400, 500)  # Set fixed size for the form

        # Main layout
        main_layout = QVBoxLayout()

        # Top layout for logo and greeting
        top_layout = QHBoxLayout()

        # Logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap('logo.png')  # Load the logo image
        logo_pixmap = logo_pixmap.scaled(QSize(150, 150), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        top_layout.addWidget(logo_label)

        # Greeting
        greeting_label = QLabel('Bonjour !')
        greeting_label.setFont(QFont('Arial', 18))
        top_layout.addWidget(greeting_label)

        # Spacer to push the greeting to the left
        top_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        main_layout.addLayout(top_layout)

        # Username Field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Votre Nom')
        self.username_input.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        main_layout.addWidget(self.username_input)

        # Password Field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Mot De Passe')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")
        main_layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QPushButton('Login')
        self.login_button.setStyleSheet(
            "font-size: 18px; padding: 10px; background-color: #0078d4; color: white; border-radius: 5px;")
        self.login_button.clicked.connect(self.login)
        main_layout.addWidget(self.login_button)

        # Register Button
        self.register_button = QPushButton('Sign Up')
        self.register_button.setStyleSheet(
            "font-size: 18px; padding: 10px; background-color: #0078d4; color: white; border-radius: 5px;")
        self.register_button.clicked.connect(self.register)
        main_layout.addWidget(self.register_button)

        # Register Link
        register_label = QLabel('')
        register_label.setStyleSheet("font-size: 5px; color: blue;")
        register_label.setAlignment(Qt.AlignCenter)
        register_label.setOpenExternalLinks(True)
        main_layout.addWidget(register_label)

        self.setLayout(main_layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            QMessageBox.information(self, 'Login', 'Login successful!')
            self.main_menu = MainMenu(username)  # Pass username to MainMenu
            self.main_menu.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Login', 'Incorrect username or password.')

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'Register', 'Registration successful!')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())
