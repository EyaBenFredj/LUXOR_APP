import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QFormLayout, QRadioButton, QButtonGroup
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
import sqlite3


class AddProduct(QWidget):
    product_added = pyqtSignal()  # Signal to notify product addition

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add Product')
        self.setGeometry(100, 100, 600, 600)

        # Set fonts
        label_font = QFont()
        label_font.setPointSize(16)
        option_font = QFont()
        option_font.setPointSize(12)

        # Set styles
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
            }
            QLineEdit, QComboBox {
                font-size: 16px;
                font-size: 16px;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QRadioButton {
                font-size: 18px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 18px;
                padding: 10px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        # Layouts
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Code
        self.code_label = QLabel('Code:')
        self.code_label.setFont(label_font)
        self.code_input = QLineEdit()

        # Nom du produit
        self.nom_label = QLabel('Nom du produit:')
        self.nom_label.setFont(label_font)
        self.nom_input = QLineEdit()

        # Fournisseur
        self.fournisseur_label = QLabel('Fournisseur:')
        self.fournisseur_label.setFont(label_font)
        self.fournisseur_input = QLineEdit()

        # Unité
        self.unite_label = QLabel('Unité:')
        self.unite_label.setFont(label_font)
        self.unite_input = QComboBox()
        self.unite_input.addItems(['Kg', 'L'])
        self.unite_input.setEditable(True)

        # Colisage
        self.colisage_label = QLabel('Colisage:')
        self.colisage_label.setFont(label_font)
        self.colisage_input = QLineEdit()

        # Devise
        self.devise_label = QLabel('Devise:')
        self.devise_label.setFont(label_font)
        self.devise_input = QComboBox()
        self.devise_input.addItems(['USD', 'EUR'])
        self.devise_input.setEditable(True)

        # Quantité par palette
        self.qte_palette_label = QLabel('Quantité par palette:')
        self.qte_palette_label.setFont(label_font)
        self.qte_palette_input = QLineEdit()

        # Conteneurs 20' and 40'
        self.conteneur_label = QLabel("Conteneurs:")
        self.conteneur_label.setFont(label_font)
        self.conteneur_20_input = QLineEdit()
        self.conteneur_20_input.setPlaceholderText("20'")
        self.conteneur_40_input = QLineEdit()
        self.conteneur_40_input.setPlaceholderText("40'")
        conteneur_layout = QHBoxLayout()
        conteneur_layout.addWidget(self.conteneur_20_input)
        conteneur_layout.addWidget(self.conteneur_40_input)

        # Autorisation
        self.autorisation_label = QLabel('Autorisation:')
        self.autorisation_label.setFont(label_font)
        self.autorisation_input = QComboBox()
        self.autorisation_input.addItems(['677', '626'])
        self.autorisation_input.setEditable(True)

        # Position Tarifaire
        self.position_tarifaire_label = QLabel('Position Tarifaire:')
        self.position_tarifaire_label.setFont(label_font)
        self.position_tarifaire_input = QLineEdit()

        # Droits et Taxes
        self.droits_taxes_label = QLabel('Droits et Taxes:')
        self.droits_taxes_label.setFont(label_font)
        self.droits_taxes_input = QLineEdit()

        # EUR1
        self.eur1_label = QLabel('EUR1:')
        self.eur1_label.setFont(label_font)
        self.eur1_yes_radio = QRadioButton('Oui')
        self.eur1_yes_radio.setFont(option_font)
        self.eur1_no_radio = QRadioButton('Non')
        self.eur1_no_radio.setFont(option_font)
        self.eur1_group = QButtonGroup()
        self.eur1_group.addButton(self.eur1_yes_radio)
        self.eur1_group.addButton(self.eur1_no_radio)
        eur1_layout = QHBoxLayout()
        eur1_layout.addWidget(self.eur1_yes_radio)
        eur1_layout.addWidget(self.eur1_no_radio)

        # Incoterm
        self.incoterm_label = QLabel('Incoterm:')
        self.incoterm_label.setFont(label_font)
        self.incoterm_input = QComboBox()
        self.incoterm_input.addItems(['EXW', 'FCA', 'FCR'])
        self.incoterm_input.setEditable(True)

        # Pelletisation
        self.pelletisation_label = QLabel('Pelletisation:')
        self.pelletisation_label.setFont(label_font)
        self.pelletisation_gerbable_radio = QRadioButton('Gerbable')
        self.pelletisation_gerbable_radio.setFont(option_font)
        self.pelletisation_non_gerbable_radio = QRadioButton('Non Gerbable')
        self.pelletisation_non_gerbable_radio.setFont(option_font)
        self.pelletisation_group = QButtonGroup()
        self.pelletisation_group.addButton(self.pelletisation_gerbable_radio)
        self.pelletisation_group.addButton(self.pelletisation_non_gerbable_radio)
        pelletisation_layout = QHBoxLayout()
        pelletisation_layout.addWidget(self.pelletisation_gerbable_radio)
        pelletisation_layout.addWidget(self.pelletisation_non_gerbable_radio)

        # Libre
        self.libre_label = QLabel('Libre:')
        self.libre_label.setFont(label_font)
        self.libre_yes_radio = QRadioButton('Oui')
        self.libre_yes_radio.setFont(option_font)
        self.libre_no_radio = QRadioButton('Non')
        self.libre_no_radio.setFont(option_font)
        self.libre_group = QButtonGroup()
        self.libre_group.addButton(self.libre_yes_radio)
        self.libre_group.addButton(self.libre_no_radio)
        libre_layout = QHBoxLayout()
        libre_layout.addWidget(self.libre_yes_radio)
        libre_layout.addWidget(self.libre_no_radio)

        # Origine
        self.origine_label = QLabel('Origine:')
        self.origine_label.setFont(label_font)
        self.origine_input = QComboBox()
        self.origine_input.addItems(['France', 'Belgique', 'Espagne', 'Chine'])
        self.origine_input.setEditable(True)

        # Timbre
        self.timbre_label = QLabel('Timbre:')
        self.timbre_label.setFont(label_font)
        self.timbre_input = QComboBox()
        self.timbre_input.addItems(['9', '27'])
        self.timbre_input.setEditable(True)

        # Add Button
        self.add_button = QPushButton('Add the Product')
        self.add_button.setStyleSheet(
            'QPushButton {background-color: #007bff; color: white; font-size: 14pt; padding: 10px; border: none; border-radius: 4px;}')
        self.add_button.clicked.connect(self.add_product)

        # Adding widgets to layout
        form_layout.addRow(self.code_label, self.code_input)
        form_layout.addRow(self.nom_label, self.nom_input)
        form_layout.addRow(self.fournisseur_label, self.fournisseur_input)
        form_layout.addRow(self.unite_label, self.unite_input)
        form_layout.addRow(self.colisage_label, self.colisage_input)
        form_layout.addRow(self.devise_label, self.devise_input)
        form_layout.addRow(self.qte_palette_label, self.qte_palette_input)
        form_layout.addRow(self.conteneur_label, conteneur_layout)
        form_layout.addRow(self.autorisation_label, self.autorisation_input)
        form_layout.addRow(self.position_tarifaire_label, self.position_tarifaire_input)
        form_layout.addRow(self.droits_taxes_label, self.droits_taxes_input)
        form_layout.addRow(self.eur1_label, eur1_layout)
        form_layout.addRow(self.incoterm_label, self.incoterm_input)
        form_layout.addRow(self.pelletisation_label, pelletisation_layout)
        form_layout.addRow(self.libre_label, libre_layout)
        form_layout.addRow(self.origine_label, self.origine_input)
        form_layout.addRow(self.timbre_label, self.timbre_input)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def add_product(self):
        # Get values from inputs
        code = self.code_input.text()
        nom = self.nom_input.text()
        fournisseur = self.fournisseur_input.text()
        unite = self.unite_input.currentText()
        colisage = self.colisage_input.text()
        devise = self.devise_input.currentText()
        qte_palette = self.qte_palette_input.text()
        conteneur_20 = self.conteneur_20_input.text()
        conteneur_40 = self.conteneur_40_input.text()
        autorisation = self.autorisation_input.currentText()
        position_tarifaire = self.position_tarifaire_input.text()
        droits_taxes = self.droits_taxes_input.text()
        eur1 = 'Yes' if self.eur1_yes_radio.isChecked() else 'No'
        incoterm = self.incoterm_input.currentText()
        pelletisation = 'Gerbable' if self.pelletisation_gerbable_radio.isChecked() else 'Non Gerbable'
        libre = 'Yes' if self.libre_yes_radio.isChecked() else 'No'
        origine = self.origine_input.currentText()
        timbre = self.timbre_input.currentText()

        # Insert data into the database
        try:
            conn = sqlite3.connect('cost_calculation.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Products (code, nom_du_produit, fournisseur, unite, colisage, devise, qte_par_palette, conteneurs_20, conteneurs_40, autorisation, position_tarifaire, droits_taxes, eur1_on, incoterm, pelletisation, libre, origine, timbre)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            code, nom, fournisseur, unite, colisage, devise, qte_palette, conteneur_20, conteneur_40, autorisation,
            position_tarifaire, droits_taxes, eur1, incoterm, pelletisation, libre, origine, timbre))
            conn.commit()
            conn.close()
            self.product_added.emit()  # Emit signal to notify product addition
            QMessageBox.information(self, 'Success', 'Product added successfully!')
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error', f'Failed to add product: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = AddProduct()
    form.show()
    sys.exit(app.exec_())
