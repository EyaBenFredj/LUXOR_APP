import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, \
    QMessageBox, QComboBox, QCompleter
import sqlite3
import os


def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'cost_calculation.db')
    return db_path


class UpdateProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Mettre à jour un produit')
        self.setGeometry(150, 150, 400, 800)

        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
            }
            QLabel {
                color: #333;
                font-size: 16px;
            }
            QLineEdit {
                background-color: #fff;
                border: 1px solid #ccc;
                font-size: 14px;
                padding: 5px;
            }
            QComboBox {
                background-color: #fff;
                border: 1px solid #ccc;
                font-size: 14px;
                padding: 5px;
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

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        search_layout = QFormLayout()
        self.search_edit = QLineEdit()
        search_layout.addRow(QLabel('Rechercher par code, nom ou fournisseur'), self.search_edit)

        self.search_button = QPushButton('Rechercher')
        self.search_button.clicked.connect(self.search_product)
        search_layout.addRow(self.search_button)

        main_layout.addLayout(search_layout)

        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(0, 20, 0, 0)  # Add margin to separate search and update sections

        self.code_edit = QLineEdit()
        self.nom_du_produit_edit = QLineEdit()
        self.fournisseur_edit = QLineEdit()
        self.setup_fournisseur_autocomplete()
        self.unite_edit = QLineEdit()
        self.colisage_edit = QLineEdit()
        self.devise_edit = QLineEdit()
        self.qte_par_palette_edit = QLineEdit()
        self.conteneurs_20_edit = QLineEdit()
        self.conteneurs_40_edit = QLineEdit()
        self.autorisation_edit = QLineEdit()
        self.position_tarifaire_edit = QLineEdit()
        self.droits_taxes_edit = QLineEdit()
        self.eur1_on_edit = QLineEdit()
        self.incoterm_edit = QLineEdit()
        self.pelletisation_edit = QLineEdit()
        self.libre_edit = QLineEdit()
        self.origine_edit = QLineEdit()
        self.timbre_edit = QLineEdit()

        self.form_layout.addRow(QLabel('Code'), self.code_edit)
        self.form_layout.addRow(QLabel('Nom du produit'), self.nom_du_produit_edit)
        self.form_layout.addRow(QLabel('Fournisseur'), self.fournisseur_edit)
        self.form_layout.addRow(QLabel('Unité'), self.unite_edit)
        self.form_layout.addRow(QLabel('Colisage'), self.colisage_edit)
        self.form_layout.addRow(QLabel('Devise'), self.devise_edit)
        self.form_layout.addRow(QLabel('Quantité par palette'), self.qte_par_palette_edit)
        self.form_layout.addRow(QLabel('Conteneurs 20'), self.conteneurs_20_edit)
        self.form_layout.addRow(QLabel('Conteneurs 40'), self.conteneurs_40_edit)
        self.form_layout.addRow(QLabel('Autorisation'), self.autorisation_edit)
        self.form_layout.addRow(QLabel('Position tarifaire'), self.position_tarifaire_edit)
        self.form_layout.addRow(QLabel('Droits et taxes'), self.droits_taxes_edit)
        self.form_layout.addRow(QLabel('EUR1 On'), self.eur1_on_edit)
        self.form_layout.addRow(QLabel('Incoterm'), self.incoterm_edit)
        self.form_layout.addRow(QLabel('Pelletisation'), self.pelletisation_edit)
        self.form_layout.addRow(QLabel('Libre'), self.libre_edit)
        self.form_layout.addRow(QLabel('Origine'), self.origine_edit)
        self.form_layout.addRow(QLabel('Timbre'), self.timbre_edit)

        self.update_button = QPushButton('Mettre à jour')
        self.update_button.clicked.connect(self.update_product)
        self.form_layout.addRow(self.update_button)

        main_layout.addLayout(self.form_layout)
        self.form_layout.setEnabled(False)  # Disable form initially

    def setup_fournisseur_autocomplete(self):
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT fournisseur FROM Suppliers")
        suppliers = cursor.fetchall()
        conn.close()

        supplier_list = [supplier[0] for supplier in suppliers]
        completer = QCompleter(supplier_list)
        self.fournisseur_edit.setCompleter(completer)

    def search_product(self):
        search_term = self.search_edit.text()

        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        query = """
            SELECT * FROM Products 
            WHERE code = ? OR nom_du_produit LIKE ? OR fournisseur = ?
        """
        cursor.execute(query, (search_term, f"%{search_term}%", search_term))
        product = cursor.fetchone()

        if product:
            self.load_product_details(product)
            self.form_layout.setEnabled(True)
        else:
            QMessageBox.warning(self, 'Erreur', 'Produit non trouvé.')
            self.form_layout.setEnabled(False)
        conn.close()

    def load_product_details(self, product):
        (
            product_id, code, nom_du_produit, fournisseur, unite, colisage, devise, _, _, qte_par_palette,
            conteneurs_20, conteneurs_40, autorisation, position_tarifaire, droits_taxes, eur1_on, incoterm,
            pelletisation, libre, _, origine, timbre, *_
        ) = product

        self.code_edit.setText(str(code))
        self.nom_du_produit_edit.setText(nom_du_produit)
        self.fournisseur_edit.setText(fournisseur)
        self.unite_edit.setText(unite)
        self.colisage_edit.setText(colisage)
        self.devise_edit.setText(devise)
        self.qte_par_palette_edit.setText(str(qte_par_palette))
        self.conteneurs_20_edit.setText(str(conteneurs_20))
        self.conteneurs_40_edit.setText(str(conteneurs_40))
        self.autorisation_edit.setText(autorisation)
        self.position_tarifaire_edit.setText(position_tarifaire)
        self.droits_taxes_edit.setText(droits_taxes)
        self.eur1_on_edit.setText(eur1_on)
        self.incoterm_edit.setText(incoterm)
        self.pelletisation_edit.setText(pelletisation)
        self.libre_edit.setText(libre)
        self.origine_edit.setText(origine)
        self.timbre_edit.setText(str(timbre))

    def update_product(self):
        code = self.code_edit.text()
        nom_du_produit = self.nom_du_produit_edit.text()
        fournisseur = self.fournisseur_edit.text()
        unite = self.unite_edit.text()
        colisage = self.colisage_edit.text()
        devise = self.devise_edit.text()
        qte_par_palette = self.qte_par_palette_edit.text()
        conteneurs_20 = self.conteneurs_20_edit.text()
        conteneurs_40 = self.conteneurs_40_edit.text()
        autorisation = self.autorisation_edit.text()
        position_tarifaire = self.position_tarifaire_edit.text()
        droits_taxes = self.droits_taxes_edit.text()
        eur1_on = self.eur1_on_edit.text()
        incoterm = self.incoterm_edit.text()
        pelletisation = self.pelletisation_edit.text()
        libre = self.libre_edit.text()
        origine = self.origine_edit.text()
        timbre = self.timbre_edit.text()

        if not all([code, nom_du_produit, fournisseur]):
            QMessageBox.warning(self, 'Erreur', 'Les champs Code, Nom du produit et Fournisseur sont obligatoires.')
            return

        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE Products
                SET nom_du_produit=?, fournisseur=?, unite=?, colisage=?, devise=?, qte_par_palette=?, conteneurs_20=?, conteneurs_40=?, 
                    autorisation=?, position_tarifaire=?, droits_taxes=?, eur1_on=?, incoterm=?, pelletisation=?, libre=?, origine=?, timbre=?
                WHERE code=?
            ''', (
                nom_du_produit, fournisseur, unite, colisage, devise, int(qte_par_palette), int(conteneurs_20),
                int(conteneurs_40),
                autorisation, position_tarifaire, droits_taxes, eur1_on, incoterm, pelletisation, libre, origine,
                float(timbre), int(code)
            ))

            if cursor.rowcount == 0:
                QMessageBox.warning(self, 'Erreur', 'Produit non trouvé.')
            else:
                conn.commit()
                QMessageBox.information(self, 'Succès', 'Produit mis à jour avec succès.')
                self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Erreur', 'Une erreur d\'intégrité s\'est produite.')
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Une erreur s\'est produite: {e}')
        finally:
            conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    update_product_window = UpdateProductWindow()
    update_product_window.show()
    sys.exit(app.exec_())
