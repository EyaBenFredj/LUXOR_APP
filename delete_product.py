import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3

class DeleteProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Delete Product')

        # Set a modern font
        font = QFont("Arial", 14)
        self.setFont(font)

        layout = QVBoxLayout()

        # Search bar layout
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter product code, name, or fournisseur")
        search_button = QPushButton('Search')
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff; 
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        search_button.clicked.connect(self.search_product)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        layout.addLayout(search_layout)

        self.product_info = QTextEdit()
        self.product_info.setReadOnly(True)
        layout.addWidget(self.product_info)

        self.delete_button = QPushButton('Delete Product')
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545; 
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.delete_button.clicked.connect(self.delete_product)
        self.delete_button.setEnabled(False)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

        # Scale up the overall size of the window
        self.resize(900, 700)

    def search_product(self):
        search_value = self.search_input.text()
        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM Products WHERE code = ? OR nom_du_produit = ? OR fournisseur = ?
        ''', (search_value, search_value, search_value))
        self.product = cursor.fetchone()
        conn.close()

        if self.product:
            product_info = f"""
            Code: {self.product[1]}
            Name: {self.product[2]}
            Fournisseur: {self.product[3]}
            Unité: {self.product[4]}
            Colisage: {self.product[5]}
            Devise: {self.product[6]}
            Prix Unitaire: {self.product[7]}
            Volume: {self.product[8]}
            Quantité par Palette: {self.product[9]}
            Conteneurs 20': {self.product[10]}
            Conteneurs 40': {self.product[11]}
            Autorisation: {self.product[12]}
            Position Tarifaire: {self.product[13]}
            Droits et Taxes: {self.product[14]}
            EUR1: {self.product[15]}
            Incoterm: {self.product[16]}
            Pelletisation: {self.product[17]}
            Libre: {self.product[18]}
            Convention de Commerce: {self.product[19]}
            Origine: {self.product[20]}
            TIMBRE: {self.product[21]}
            Total EXW: {self.product[22]}
            Total Charge Logistique: {self.product[23]}
            Total Droits et Taxes: {self.product[24]}
            Total Frais: {self.product[25]}
            Assurance: {self.product[26]}
            DD: {self.product[27]}
            FODEC: {self.product[28]}
            TPE: {self.product[29]}
            TVA: {self.product[30]}
            RDP: {self.product[31]}
            AIR: {self.product[32]}
            ANGED: {self.product[33]}
            Fret: {self.product[34]}
            Fret d'Avis d'Arrivée: {self.product[35]}
            UC: {self.product[36]}
            Magasinage: {self.product[37]}
            Manutention: {self.product[38]}
            Transport Local: {self.product[39]}
            Honoraire de Transitaire: {self.product[40]}
            Cost Price: {self.product[41]}
            """
            self.product_info.setText(product_info)
            self.delete_button.setEnabled(True)
        else:
            self.product_info.setText("Product not found.")
            self.delete_button.setEnabled(False)

    def delete_product(self):
        code = self.product[1]
        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Products WHERE code = ?', (code,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Success', f'Product {code} deleted successfully!')
        self.product_info.clear()
        self.delete_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    delete_product_window = DeleteProduct()
    delete_product_window.show()
    sys.exit(app.exec_())
