import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
import sqlite3
import os
from add_supplier import AddSupplierWindow

def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'cost_calculation.db')
    return db_path

class SuppliersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_suppliers_data()

    def init_ui(self):
        self.setWindowTitle('Liste des Fournisseurs')
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
            }
            QLabel {
                color: #333;
                font-size: 16px;
            }
            QTableWidget {
                background-color: #fff;
                border: none;
                font-size: 14px;
                color: #333;
            }
            QHeaderView::section {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border: none;
                font-size: 14px;
            }
            QTableWidgetItem {
                padding: 10px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setRowCount(0)  # Initially empty
        self.table.setColumnCount(5)  # Five columns for fournisseurs' details
        self.table.setHorizontalHeaderLabels(['Supplier', 'Adresse de l\'usine', 'Adresse du siège', 'Devise', 'Modalité de paiement'])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table)

        # Add button for adding suppliers
        self.add_supplier_button = QPushButton('Ajouter un Fournisseur')
        self.add_supplier_button.clicked.connect(self.open_add_supplier_window)
        layout.addWidget(self.add_supplier_button)

    def load_suppliers_data(self):
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        try:
            # Fetching data from the ListeFour table
            cursor.execute('''
                SELECT supplier, adresse_usine, adresse_siege, devise, modalite_paiement 
                FROM ListeFour
            ''')
            suppliers = cursor.fetchall()

            self.table.setRowCount(len(suppliers))
            for row_idx, row_data in enumerate(suppliers):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_idx, col_idx, item)

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

        finally:
            conn.close()

    def open_add_supplier_window(self):
        self.add_supplier_window = AddSupplierWindow()
        self.add_supplier_window.show()
        self.add_supplier_window.closeEvent = self.handle_add_supplier_close

    def handle_add_supplier_close(self, event):
        self.load_suppliers_data()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    suppliers_window = SuppliersWindow()
    suppliers_window.show()
    sys.exit(app.exec_())
