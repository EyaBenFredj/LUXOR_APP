import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from fpdf import FPDF
from datetime import datetime


class Imprimer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle('Imprimer Un Document')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Search bar layout
        search_layout = QHBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher par code ou nom...")
        self.search_bar.setFont(QFont("Arial", 14))
        self.search_bar.setMinimumWidth(400)
        self.search_bar.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_bar)

        # Search button
        search_button = QPushButton('Rechercher')
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f7f;
            }
        """)
        search_button.clicked.connect(lambda: self.filter_table(self.search_bar.text()))
        search_layout.addWidget(search_button)

        main_layout.addLayout(search_layout)

        # Selection instruction label
        self.selection_label = QLabel('Sélectionner les données à Imprimer ')
        self.selection_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(self.selection_label)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Code', 'Nom du produit', 'Fournisseur', 'Prix unitaire', 'Cost Price'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)
        main_layout.addWidget(self.table)

        # Print buttons
        self.print_table_button = QPushButton('Imprimer Le Tableau')
        self.print_table_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f7f;
            }
        """)
        self.print_table_button.clicked.connect(self.print_table_pdf)
        main_layout.addWidget(self.print_table_button)

        self.print_details_button = QPushButton('Imprimer Les Détails Des Produits')
        self.print_details_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f7f;
            }
        """)
        self.print_details_button.clicked.connect(self.print_details_pdf)
        main_layout.addWidget(self.print_details_button)

    def load_data(self):
        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()

        cursor.execute('SELECT code, nom_du_produit, fournisseur, prix_unitaire, cost_price FROM Products')
        self.data = cursor.fetchall()

        self.display_data(self.data)

        conn.close()

    def display_data(self, data):
        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row_idx, col_idx, item)

    def filter_table(self, text):
        filtered_data = [
            item for item in self.data
            if text.lower() in str(item[0]).lower() or text.lower() in str(item[1]).lower()
        ]
        self.display_data(filtered_data)

    def print_table_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.generate_table_pdf(file_path)

    def print_details_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.generate_details_pdf(file_path)

    def generate_table_pdf(self, file_path):
        pdf = FPDF()
        pdf.add_page()

        # Add company logo
        pdf.image('logo.png', x=10, y=8, w=33)

        # Add date
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=datetime.now().strftime("%Y-%m-%d"), ln=True, align='R')

        pdf.ln(10)  # Add a line break

        # Add document title
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt="Liste des Produits", ln=True, align='C')

        pdf.ln(10)  # Add a line break

        # Table headers
        headers = ['Code', 'Nom du produit', 'Fournisseur', 'Prix unitaire', 'Cost Price']
        pdf.set_font("Arial", size=12)
        for header in headers:
            pdf.cell(40, 10, header, 1, 0, 'C')
        pdf.ln()

        # Table data
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                pdf.cell(40, 10, self.table.item(row, col).text(), 1, 0, 'C')
            pdf.ln()

        # Add a bottom margin
        pdf.cell(0, 20, '', 0, 1, 'C')

        pdf.output(file_path)

    def generate_details_pdf(self, file_path):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        selected_rows = set()
        for item in selected_items:
            selected_rows.add(item.row())

        if not selected_rows:
            return

        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()

        # Fetch data for selected products
        selected_data = []
        for row in selected_rows:
            code_item = self.table.item(row, 0)
            if code_item:
                code = code_item.text()
                cursor.execute('SELECT * FROM Products WHERE code = ?', (code,))
                selected_data.append(cursor.fetchone())

        columns = [description[0] for description in cursor.description]

        conn.close()

        pdf = FPDF()
        pdf.add_page()

        # Add company logo
        pdf.image('logo.png', x=10, y=8, w=33)

        # Add date
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=datetime.now().strftime("%Y-%m-%d"), ln=True, align='R')

        pdf.ln(10)  # Add a line break

        # Add document title
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt="Détails des Produits", ln=True, align='C')

        pdf.ln(10)  # Add a line break

        # Detailed product data
        pdf.set_font("Arial", size=10)
        for row in selected_data:
            for col, item in zip(columns, row):
                pdf.multi_cell(0, 10, f"{col}: {item}")
            pdf.ln(10)  # Add space between products

        pdf.output(file_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Imprimer()
    window.show()
    sys.exit(app.exec_())
