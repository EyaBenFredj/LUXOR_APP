import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
import sqlite3
import os

def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'cost_calculation.db')
    return db_path

class AddSupplierWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Ajouter un Fournisseur')
        self.setGeometry(200, 200, 500, 300)

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

        layout = QFormLayout()
        self.setLayout(layout)

        self.supplier_edit = QLineEdit()
        self.adresse_usine_edit = QLineEdit()
        self.adresse_siege_edit = QLineEdit()
        self.devise_edit = QLineEdit()
        self.modalite_paiement_edit = QLineEdit()

        layout.addRow(QLabel('Fournisseur : '), self.supplier_edit)
        layout.addRow(QLabel('Adresse de l\'usine :'), self.adresse_usine_edit)
        layout.addRow(QLabel('Adresse du siège : '), self.adresse_siege_edit)
        layout.addRow(QLabel('Devise :'), self.devise_edit)
        layout.addRow(QLabel('Modalité de paiement :'), self.modalite_paiement_edit)

        self.add_button = QPushButton('Ajouter Le Fournisseur')
        self.add_button.clicked.connect(self.add_supplier)
        layout.addRow(self.add_button)

    def add_supplier(self):
        supplier = self.supplier_edit.text()
        adresse_usine = self.adresse_usine_edit.text()
        adresse_siege = self.adresse_siege_edit.text()
        devise = self.devise_edit.text()
        modalite_paiement = self.modalite_paiement_edit.text()

        if not all([supplier, adresse_usine, adresse_siege, devise, modalite_paiement]):
            QMessageBox.warning(self, 'Erreur', 'Tous les champs sont obligatoires.')
            return

        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO ListeFour (supplier, adresse_usine, adresse_siege, devise, modalite_paiement)
                VALUES (?, ?, ?, ?, ?)
            ''', (supplier, adresse_usine, adresse_siege, devise, int(modalite_paiement)))

            conn.commit()
            QMessageBox.information(self, 'Succès', 'Fournisseur ajouté avec succès.')
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Erreur', 'Ce fournisseur existe déjà.')
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Une erreur s\'est produite: {e}')
        finally:
            conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    add_supplier_window = AddSupplierWindow()
    add_supplier_window.show()
    sys.exit(app.exec_())
