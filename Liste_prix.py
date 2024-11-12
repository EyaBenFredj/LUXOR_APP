import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt5.QtCore import Qt

class ListePrix(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Liste Prix de Revient')
        self.setGeometry(100, 100, 800, 600)  # Adjust size as needed

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Entrez un code ou nom...")
        self.search_bar.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_bar)
        main_layout.addLayout(search_layout)

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Code', 'Nom', 'Prix de Revient'])
        self.table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table)

        self.load_product_data()

    def load_product_data(self):
        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()

        cursor.execute('SELECT code, nom_du_produit, cost_price FROM Products')
        self.products = cursor.fetchall()

        self.display_products(self.products)

        conn.close()

    def display_products(self, products):
        self.table.setRowCount(len(products))
        for row_idx, row_data in enumerate(products):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def filter_table(self, text):
        filtered_products = [
            product for product in self.products
            if text.lower() in str(product[0]).lower() or
               text.lower() in str(product[1]).lower()
        ]
        self.display_products(filtered_products)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    liste_prix = ListePrix()
    liste_prix.show()
    sys.exit(app.exec_())
