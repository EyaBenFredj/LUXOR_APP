import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt5.QtGui import QFont
import sqlite3
import os


class FicheTechnique(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Fiche Technique')
        self.setGeometry(100, 100, 1000, 600)  # Widen the form

        main_layout = QVBoxLayout()

        # Set global font size
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

        # Search Bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Entrez un code, nom, ou fournisseur')
        self.search_input.setFont(QFont("Arial", 12))  # Set font size for the search bar
        self.search_input.setFixedHeight(40)  # Increase the height of the search bar
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton('Search', self)
        self.search_button.setFont(QFont("Arial", 12))  # Set font size for the search button
        self.search_button.setFixedHeight(40)  # Increase the height of the search button
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #3399ff;  /* Lighter blue color */
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1e90ff;  /* Darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #007acc;  /* Even darker blue when pressed */
            }
        """)  # Set button color to lighter blue
        self.search_button.clicked.connect(self.search_products)
        search_layout.addWidget(self.search_button)

        main_layout.addLayout(search_layout)

        # Results Table
        self.results_table = QTableWidget(self)
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(['Code', 'Nom', 'Fournisseur', 'Fiche', 'Action'])
        self.results_table.horizontalHeader().setFont(QFont("Arial", 11))  # Set font size for table headers
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.results_table)

        # Message Label
        self.message_label = QLabel('', self)
        self.message_label.setFont(QFont("Arial", 11))  # Set font size for the message label
        main_layout.addWidget(self.message_label)

        self.setLayout(main_layout)

    def search_products(self):
        search_text = self.search_input.text().strip()
        if not search_text:
            self.show_message('Please enter a search term.')
            return

        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
            SELECT code, nom_du_produit, fournisseur
            FROM Products
            WHERE code LIKE ? OR nom_du_produit LIKE ? OR fournisseur LIKE ?
            ''', (f'%{search_text}%', f'%{search_text}%', f'%{search_text}%'))

            products = cursor.fetchall()
            conn.close()

            if products:
                self.results_table.setRowCount(len(products))
                for row, product in enumerate(products):
                    code, nom, fournisseur = product
                    pdf_status = self.check_pdf_status(code)
                    self.results_table.setItem(row, 0, QTableWidgetItem(str(code)))
                    self.results_table.setItem(row, 1, QTableWidgetItem(nom))
                    self.results_table.setItem(row, 2, QTableWidgetItem(fournisseur))
                    self.results_table.setItem(row, 3, QTableWidgetItem('Exists' if pdf_status else 'Not Exists'))
                    action_button = QPushButton('Voir PDF' if pdf_status else 'Charger PDF', self)

                    self.results_table.setItem(row, 4, QTableWidgetItem('Exists' if pdf_status else 'Not Exists'))
                    action_button = QPushButton('Voir PDF' if pdf_status else 'Charger PDF', self)
                    action_button.setFont(QFont("Arial", 14))  # Set font size for action buttons
                    action_button.setStyleSheet("""
                        QPushButton {
                            background-color: #3399ff;  /* Lighter blue color */
                            color: white;
                            border: none;
                            padding: 10px;
                            border-radius: 5px;
                            min-width: 180px;  /* Set a minimum width for the buttons, 1.5 times wider */
                        }
                        QPushButton:hover {
                            background-color: #1e90ff;  /* Darker blue on hover */
                        }
                        QPushButton:pressed {
                            background-color: #007acc;  /* Even darker blue when pressed */
                        }
                    """)  # Set button color to lighter blue
                    action_button.clicked.connect(self.create_pdf_action_handler(code))
                    self.results_table.setCellWidget(row, 4, action_button)
                    self.results_table.setRowHeight(row, 50)  # Make the rows a bit larger
            else:
                self.results_table.setRowCount(0)
                self.show_message('No products found.')
        except sqlite3.Error as e:
            self.show_message(f'Database error: {e}')
            print(f'Database error: {e}')

    def create_pdf_action_handler(self, code):
        return lambda checked: self.handle_pdf_action(code)

    def check_pdf_status(self, code):
        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
            SELECT 1
            FROM ProductPDFs
            WHERE code = ?
            ''', (code,))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except sqlite3.Error as e:
            self.show_message(f'Database error: {e}')
            print(f'Database error: {e}')
            return False

    def handle_pdf_action(self, code):
        pdf_status = self.check_pdf_status(code)
        if (pdf_status):
            self.view_pdf(code)
        else:
            self.upload_pdf(code)

    def view_pdf(self, code):
        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
            SELECT pdf_data
            FROM ProductPDFs
            WHERE code = ?
            ''', (code,))
            result = cursor.fetchone()
            conn.close()

            if result:
                pdf_data = result[0]
                temp_pdf_path = f'{code}_temp.pdf'
                with open(temp_pdf_path, 'wb') as file:
                    file.write(pdf_data)
                os.startfile(temp_pdf_path)
            else:
                self.show_message('PDF not found.')
        except sqlite3.Error as e:
            self.show_message(f'Database error: {e}')
            print(f'Database error: {e}')

    def upload_pdf(self, code):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, 'Open PDF', '', 'PDF Files (*.pdf)')
        if file_path:
            with open(file_path, 'rb') as file:
                pdf_data = file.read()

            conn = sqlite3.connect('cost_calculation.db')
            cursor = conn.cursor()
            try:
                cursor.execute('''
                INSERT INTO ProductPDFs (code, nom, fournisseur, pdf_data)
                VALUES ((SELECT code FROM Products WHERE code = ?), (SELECT nom_du_produit FROM Products WHERE code = ?), (SELECT fournisseur FROM Products WHERE code = ?), ?)
                ''', (code, code, code, pdf_data))

                conn.commit()
                conn.close()

                self.show_message('PDF uploaded successfully.')
                self.search_products()
            except sqlite3.Error as e:
                self.show_message(f'Database error: {e}')
                print(f'Database error: {e}')

    def show_message(self, message):
        self.message_label.setText(message)
        QMessageBox.information(self, 'Info', message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fiche_technique = FicheTechnique()
    fiche_technique.show()
    sys.exit(app.exec_())
