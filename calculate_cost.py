import sqlite3
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from database import get_db_path  # Import get_db_path from your database module


# Fetch product details from the database
def fetch_product_details(value):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    cursor.execute("""
    SELECT code, nom_du_produit, fournisseur, unite, colisage, devise, qte_par_palette, conteneurs_20, conteneurs_40, autorisation, 
           position_tarifaire, droits_taxes, eur1_on, incoterm, pelletisation, libre, origine, timbre
    FROM Products 
    WHERE code = ? OR nom_du_produit = ? OR fournisseur = ?
    """, (value, value, value))
    product = cursor.fetchone()

    conn.close()
    return product


# Save cost price to the database
def save_cost_price(code, cost_price):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE Products
    SET cost_price = ?
    WHERE code = ?
    """, (cost_price, code))

    conn.commit()
    conn.close()


# Calculate cost price based on user inputs
def calculate_cost_price(window):
    try:
        # Extracting user inputs
        total_exw = float(window.total_exw_var.text())
        taux_de_change = float(window.taux_de_change_var.text())
        fret = float(window.fret_var.text())
        assurance = float(window.assurance_var.text())
        dd = float(window.dd_var.text())
        fodec = float(window.fodec_var.text())
        tpe = float(window.tpe_var.text())
        tva = float(window.tva_var.text())
        rdp = float(window.rdp_var.text())
        air = float(window.air_var.text())
        anged = float(window.anged_var.text())
        uc1 = float(window.uc1_var.text())
        uc2 = float(window.uc2_var.text())
        uc3 = float(window.uc3_var.text())
        magasinage = float(window.magasinage_var.text())
        manutention = float(window.manutention_var.text())
        transport_local1 = float(window.transport_local1_var.text())
        transport_local2 = float(window.transport_local2_var.text())

        # Implementing calculation logic based on the provided image
        A = total_exw * taux_de_change
        B = fret * taux_de_change
        C = (A + B) * assurance
        D = (A + B + C) * dd
        E = (D + C + B + A) * fodec
        F = (E + D + C + B + A) * tpe
        G = (F + E + D + C + B + A) * tva
        H = (RDP := G + F + E + D + C + B + A) * rdp
        I = 9  # Timbre is constant
        J = (A + B + C + D + E + F + G + H + I) * air
        K = 100 * uc1 + 200 * uc2 + 19 * uc3
        L = transport_local1 + transport_local2
        M = manutention
        N = magasinage

        total_frais = A + B + C + D + E + F + G + H + I + J + K + L + M + N
        window.cost_price_var.setText(str(total_frais))

        # Save the cost price to the database
        code = window.product_vars[0].text()
        save_cost_price(code, total_frais)

    except ValueError:
        QtWidgets.QMessageBox.critical(window, "Input Error", "Please enter valid numeric values")


# Search product by code, name, or supplier
def search_product(window):
    search_value = window.search_entry.text()

    product = fetch_product_details(search_value)

    if product:
        for i, var in enumerate(product):
            window.product_vars[i].setText(str(var))
    else:
        QtWidgets.QMessageBox.critical(window, "Search Error", "Product not found")


class CalculateCostWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculate Cost Price")
        self.setGeometry(100, 50, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.layout = QtWidgets.QVBoxLayout(self)

        # Search bar setup
        self.search_frame = QtWidgets.QFrame(self)
        self.search_frame.setStyleSheet("background-color: #f0f0f0; padding: 10px;")
        self.search_layout = QtWidgets.QHBoxLayout(self.search_frame)

        self.search_entry = QtWidgets.QLineEdit(self.search_frame)
        self.search_entry.setStyleSheet("padding: 10px; font-size: 14px; background-color: white;")
        self.search_layout.addWidget(self.search_entry)

        self.search_button = QtWidgets.QPushButton("Search", self.search_frame)
        self.search_button.setStyleSheet(
            "background-color: #0275d8; color: white; font-size: 14px; padding: 10px; border: none;")
        self.search_button.clicked.connect(lambda: search_product(self))
        self.search_layout.addWidget(self.search_button)

        self.layout.addWidget(self.search_frame)

        # Single tab with a compact layout for all fields
        self.fields_frame = QtWidgets.QFrame(self)
        self.fields_layout = QtWidgets.QGridLayout(self.fields_frame)

        product_labels = ["Code", "Nom", "Fournisseur", "Unite", "Colisage", "Devise", "Qte Palette", "Conteneur 20",
                          "Conteneur 40", "Autorisation", "Position Tarifaire", "Droits Taxes", "Eur1", "Incoterm",
                          "Pelletisation", "Libre", "Origine", "Timbre"]
        self.product_vars = [QtWidgets.QLineEdit(self.fields_frame) for _ in product_labels]

        for i, (label, var) in enumerate(zip(product_labels, self.product_vars)):
            row = i // 2
            col = (i % 2) * 2
            lbl = QtWidgets.QLabel(label, self.fields_frame)
            lbl.setStyleSheet("font-size: 14px;")
            self.fields_layout.addWidget(lbl, row, col)
            var.setReadOnly(True)
            var.setStyleSheet("font-size: 14px; padding: 5px; background-color: white;")
            self.fields_layout.addWidget(var, row, col + 1)

        fields = [
            ("Valeur EXW", 2020, "total_exw_var"),
            ("Taux de change", 3.42, "taux_de_change_var"),
            ("FRET", 0.0, "fret_var"),
            ("Assurance", 0.082, "assurance_var"),
            ("Droit de Douane", 0.3, "dd_var"),
            ("FODEC", 0.01, "fodec_var"),
            ("TPE", 0.07, "tpe_var"),
            ("TVA", 0.19, "tva_var"),
            ("RDP", 0.03, "rdp_var"),
            ("AIR", 0.1, "air_var"),
            ("Anged", 0.2, "anged_var"),
            ("UC 20'", 100, "uc1_var"),
            ("UC 40'", 200, "uc2_var"),
            ("UC +", 19, "uc3_var"),
            ("Magasinage", 0.0, "magasinage_var"),
            ("Manutention", 0.0, "manutention_var"),
            ("frais locaux 20'", 350, "transport_local1_var"),
            ("frais locaux 40'", 450, "transport_local2_var")
        ]

        for i, (label, default, var_name) in enumerate(fields):
            var = QtWidgets.QLineEdit(self.fields_frame)
            var.setText(str(default))
            var.setStyleSheet("font-size: 14px; padding: 5px; background-color: white;")
            setattr(self, var_name, var)
            row = (i + len(product_labels)) // 2
            col = ((i + len(product_labels)) % 2) * 2
            lbl = QtWidgets.QLabel(label, self.fields_frame)
            lbl.setStyleSheet("font-size: 14px;")
            self.fields_layout.addWidget(lbl, row, col)
            self.fields_layout.addWidget(var, row, col + 1)

        self.layout.addWidget(self.fields_frame)

        # Cost price calculation result
        self.result_frame = QtWidgets.QFrame(self)
        self.result_frame.setStyleSheet("background-color: #f0f0f0; padding: 10px;")
        self.result_layout = QtWidgets.QHBoxLayout(self.result_frame)

        self.cost_price_var = QtWidgets.QLineEdit(self.result_frame)
        self.cost_price_var.setReadOnly(True)
        self.cost_price_var.setStyleSheet("font-size: 14px; padding: 5px; background-color: white;")

        self.result_layout.addWidget(QtWidgets.QLabel("Cost Price:", self.result_frame))
        self.result_layout.addWidget(self.cost_price_var)

        self.calculate_button = QtWidgets.QPushButton("Calculate", self.result_frame)
        self.calculate_button.setStyleSheet(
            "background-color: #0275d8; color: white; font-size: 14px; padding: 10px; border: none;")
        self.calculate_button.clicked.connect(lambda: calculate_cost_price(self))

        self.result_layout.addWidget(self.calculate_button)
        self.layout.addWidget(self.result_frame)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = CalculateCostWindow()
    window.show()
    app.exec_()
