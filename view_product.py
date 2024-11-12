import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QHeaderView, QHBoxLayout
import sqlite3


class ViewProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('View Products')

        layout = QVBoxLayout()

        # Search bar layout
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search_products)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        layout.addLayout(search_layout)

        # Table to display products
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_data()

    def load_data(self, filter_text=''):
        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()

        if filter_text:
            cursor.execute('''
            SELECT * FROM Products WHERE code LIKE ? OR produit LIKE ? OR fournisseur LIKE ?
            ''', (f'%{filter_text}%', f'%{filter_text}%', f'%{filter_text}%'))
        else:
            cursor.execute('SELECT * FROM Products')

        products = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(products))
        self.table.setColumnCount(39)

        headers = [
            'ID', 'Code', 'Produit', 'Fournisseur', 'Unité', 'Colisage', 'Devise', 'Prix Unitaire',
            'Volume', 'Quantité par Palette', 'Autorisation', 'Position Tarifaire', 'Droits et Taxes',
            'EUR1-O/N', 'Incoterm', 'Pelletisation', 'Libre', 'Convention de Commerce', 'Origine',
            'Total EXW', 'Total charge logistique', 'Total Droits et Taxes', 'Total frais', 'Assurance',
            'DD', 'FODEC', 'TPE', 'TVA', 'RDP', 'Timbre', 'AIR', 'ANGED', 'Fret', 'Fret d\'avis d\'arrivée',
            'UC', 'Magasinage', 'Manutention', 'Transport Local', 'Honoraire de transitaire', 'Cost Price'
        ]

        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row_idx, row_data in enumerate(products):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def search_products(self):
        filter_text = self.search_input.text()
        self.load_data(filter_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view_product_window = ViewProduct()
    view_product_window.show()
    sys.exit(app.exec_())
