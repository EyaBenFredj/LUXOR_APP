import sqlite3
import os

def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'cost_calculation.db')
    return db_path

def populate_suppliers():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    suppliers_data = [
        ('Supplier A', 'Usine A', 'Siège A', 'USD', 1),
        ('Supplier B', 'Usine B', 'Siège B', 'EUR', 2),
        ('Supplier C', 'Usine C', 'Siège C', 'GBP', 3),
    ]

    cursor.executemany('''
    INSERT OR REPLACE INTO Suppliers (fournisseur, adresse_usine, adresse_siege, devise, modalite_paiement)
    VALUES (?, ?, ?, ?, ?)
    ''', suppliers_data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_suppliers()
