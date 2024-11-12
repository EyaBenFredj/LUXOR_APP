import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QFrame, QSpacerItem, QSizePolicy, QStyle
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt

from add_product import AddProduct
from update_product import UpdateProductWindow
from view_product import ViewProduct
from delete_product import DeleteProduct
from four_table import SuppliersWindow
from fiche_technique import FicheTechnique
from Liste_prix import ListePrix
from Imprimer import Imprimer
from calculate_cost import CalculateCostWindow  # Ensure this import matches the class name

class MainMenu(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()
        self.load_product_data()

    def init_ui(self):
        self.setWindowTitle('Main Menu')
        self.setGeometry(100, 100, 1200, 800)

        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
            }
            QLabel {
                color: #333;
                font-size: 16px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 15px;
                padding: 15px;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f7f;
            }
            .header-label {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
            .table-header {
                background-color: #d3d3d3;
                color: #333;
                font-size: 20px;
                padding: 10px;
                border-radius: 5px;
            }
            .table-cell {
                background-color: #ffffff;
                padding: 10px;
                border: 1px solid #ddd;
                font-size: 16px;
            }
            .sidebar-button {
                background-color: #007bff;
                color: white;
                border-radius: 15px;
                padding: 15px;
                font-size: 18px;
                border: none;
            }
            .sidebar-button:hover {
                background-color: #0056b3;
            }
            .sidebar-button:pressed {
                background-color: #003f7f;
            }
            QTableWidget {
                background-color: #fff;
                border: none;
                font-size: 14px;
                color: #333;
            }
            QHeaderView::section {
                background-color: #d3d3d3;
                color: #333;
                padding: 10px;
                border: none;
                font-size: 15px;
            }
            QTableWidgetItem {
                padding: 10px;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignTop)
        sidebar.setContentsMargins(10, 20, 10, 20)
        sidebar.setSpacing(15)
        main_layout.addLayout(sidebar, 1)

        # User Image and Label
        user_layout = QHBoxLayout()
        user_image = QLabel()
        user_pixmap = QPixmap('user.png')  # Adjust path to user image
        user_image.setPixmap(user_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        user_layout.addWidget(user_image)

        user_label = QLabel(self.username)  # Use the username here
        user_label.setAlignment(Qt.AlignCenter)
        user_label.setStyleSheet("font-size: 25px; font-weight: ;")
        user_layout.addWidget(user_label)
        sidebar.addLayout(user_layout)

        # Sidebar buttons
        sidebar_buttons = [
            (' Liste des Fournisseurs', QStyle.SP_DirOpenIcon, self.show_suppliers),
            (' Fiches Techniques', QStyle.SP_FileDialogDetailedView, self.show_tech_sheets),
            (' Liste Prix de Revient', 'money.png', self.show_cost_prices),  # Custom icon for money
            (' Imprimer Un Doc', 'pdf.png', self.show_print_doc),  # Custom icon for PDF

        ]

        for text, icon, callback in sidebar_buttons:
            button = QPushButton(text)
            button.setObjectName('sidebar-button')
            if isinstance(icon, str):  # If the icon is a custom file path
                button.setIcon(QIcon(icon))
            else:
                button.setIcon(self.style().standardIcon(icon))  # Use standard icons from QStyle
            if callback:
                button.clicked.connect(callback)
            sidebar.addWidget(button)

        # Content area
        content_area = QVBoxLayout()
        content_area.setContentsMargins(10, 10, 10, 10)
        content_area.setSpacing(10)
        main_layout.addLayout(content_area, 4)

        # Logo and Welcome Label
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignLeft)
        header_layout.setSpacing(10)

        logo_label = QLabel()
        logo_pixmap = QPixmap('logo.png')  # Adjust path to your logo image
        logo_label.setPixmap(logo_pixmap.scaled(100, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(logo_label)

        welcome_label = QLabel('Bienvenue')
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 30px; font-weight: ;")
        header_layout.addWidget(welcome_label)

        content_area.addLayout(header_layout)

        # Action buttons and search bar
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignLeft)
        buttons_layout.setSpacing(10)

        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Entrez un code, nom or fournisseur...")
        search_bar.textChanged.connect(self.filter_table)
        search_bar.setMinimumWidth(300)  # Set a minimum width for the search bar

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_bar)
        search_frame = QFrame()
        search_frame.setLayout(search_layout)

        action_buttons = [
            (' Calcul Prix de Revient', QStyle.SP_DialogApplyButton, self.calculate_cost),
            (' Ajouter Un Produit', QStyle.SP_FileDialogNewFolder, self.add_product),
            (' Mettre à jour un Produit', QStyle.SP_FileDialogDetailedView, self.update_product),
            (' Suppr Un Produit', QStyle.SP_TrashIcon, self.delete_product),
        ]

        buttons_layout.addWidget(search_frame)

        for text, icon, callback in action_buttons:
            button = QPushButton(text)
            button.setIcon(self.style().standardIcon(icon))  # Use standard icons from QStyle
            button.setStyleSheet("font-size: 18px; padding: 15px; background-color: #007bff; color: white; border-radius: 15px;")
            button.clicked.connect(callback)
            buttons_layout.addWidget(button)

        content_area.addLayout(buttons_layout)

        # Table layout
        table_layout = QVBoxLayout()

        # Table widget
        self.table = QTableWidget()
        self.table.setRowCount(0)  # Initially empty
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Code', 'Nom du produit', 'Fournisseur', 'Prix unitaire', 'Cost Price'])
        self.table.horizontalHeader().setStretchLastSection(True)

        table_layout.addWidget(self.table)
        content_area.addLayout(table_layout)

    def load_product_data(self):
        conn = sqlite3.connect('cost_calculation.db')
        cursor = conn.cursor()

        cursor.execute('SELECT code, nom_du_produit, fournisseur, prix_unitaire, cost_price FROM Products')
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
               text.lower() in str(product[1]).lower() or
               text.lower() in str(product[2]).lower()
        ]
        self.display_products(filtered_products)

    def show_suppliers(self):
        self.suppliers_window = SuppliersWindow()
        self.suppliers_window.show()

    def show_tech_sheets(self):
        self.tech_sheets_window = FicheTechnique()
        self.tech_sheets_window.show()

    def show_cost_prices(self):
        self.liste_prix_window = ListePrix()
        self.liste_prix_window.show()

    def show_print_doc(self):
        self.imprimer_window = Imprimer()
        self.imprimer_window.show()

    def add_product(self):
        self.add_product_window = AddProduct()
        self.add_product_window.product_added.connect(self.load_product_data)  # Connect signal to reload data
        self.add_product_window.show()

    def update_product(self):
        self.update_product_window = UpdateProductWindow()  # Ensure this class name matches the imported one
        self.update_product_window.show()

    def view_product(self):
        self.view_product_window = ViewProduct()
        self.view_product_window.show()

    def delete_product(self):
        self.delete_product_window = DeleteProduct()
        self.delete_product_window.show()

    def calculate_cost(self):
        self.calculate_cost_window = CalculateCostWindow()  # Ensure this class name matches the imported one
        self.calculate_cost_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu('User')  # You can pass a test username here
    main_menu.show()
    sys.exit(app.exec_())
