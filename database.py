import sqlite3
import os
import sys

def get_db_path(db_filename):
    """ Get the absolute path to the database file """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, db_filename)

def create_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    # Create Suppliers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suppliers (
        fournisseur TEXT PRIMARY KEY,
        adresse_usine TEXT,
        adresse_siege TEXT,
        devise TEXT,
        modalite_paiement INTEGER
    )
    ''')

    # Create ListeFour table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ListeFour (
        supplier TEXT PRIMARY KEY,
        adresse_usine TEXT,
        adresse_siege TEXT,
        devise TEXT,
        modalite_paiement INTEGER
    )
    ''')

    # Ensure Products table exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code INTEGER NOT NULL UNIQUE,
        nom_du_produit TEXT NOT NULL,
        fournisseur TEXT NOT NULL,
        unite TEXT,
        colisage TEXT,
        devise TEXT,
        prix_unitaire REAL,
        volume REAL,
        qte_par_palette INTEGER,
        conteneurs_20 INTEGER,
        conteneurs_40 INTEGER,
        autorisation TEXT,
        position_tarifaire TEXT,
        droits_taxes TEXT,
        eur1_on TEXT,
        incoterm TEXT,
        pelletisation TEXT,
        libre TEXT,
        convention_commerce TEXT,
        origine TEXT,
        timbre REAL,
        total_exw REAL,
        total_charge_logistique REAL,
        total_droits_et_taxes REAL,
        total_frais REAL,
        assurance REAL,
        dd REAL,
        fodec REAL,
        tpe REAL,
        tva REAL,
        rdp REAL,
        air REAL,
        anged REAL,
        fret REAL,
        fret_davis_darrivee REAL,
        uc REAL,
        magasinage REAL,
        manutention REAL,
        transport_local REAL,
        honoraire_de_transitaire REAL,
        cost_price REAL,
        FOREIGN KEY (fournisseur) REFERENCES Suppliers(fournisseur)
    )
    ''')

    # Create or alter ProductPDFs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProductPDFs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code INTEGER NOT NULL,
        nom TEXT NOT NULL,
        fournisseur TEXT NOT NULL,
        pdf_data_1 BLOB,
        pdf_data_2 BLOB,
        FOREIGN KEY (code) REFERENCES Products(code),
        FOREIGN KEY (fournisseur) REFERENCES Suppliers(fournisseur)
    )
    ''')

    conn.commit()
    conn.close()

def alter_product_pdfs_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute('''
        ALTER TABLE ProductPDFs ADD COLUMN pdf_data_1 BLOB
        ''')
    except sqlite3.OperationalError as e:
        if "duplicate column name" not in str(e):
            raise e

    try:
        cursor.execute('''
        ALTER TABLE ProductPDFs ADD COLUMN pdf_data_2 BLOB
        ''')
    except sqlite3.OperationalError as e:
        if "duplicate column name" not in str(e):
            raise e

    conn.commit()
    conn.close()

def populate_listefour(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    listefour_data = [
        ('Supplier A', 'Usine A', 'Siège A', 'USD', 1),
        ('Supplier B', 'Usine B', 'Siège B', 'EUR', 2),
        ('Supplier C', 'Usine C', 'Siège C', 'GBP', 3),
    ]

    cursor.executemany('''
    INSERT OR REPLACE INTO ListeFour (supplier, adresse_usine, adresse_siege, devise, modalite_paiement)
    VALUES (?, ?, ?, ?, ?)
    ''', listefour_data)

    conn.commit()
    conn.close()

def check_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])

    cursor.execute("PRAGMA table_info('ListeFour');")
    columns = cursor.fetchall()
    print("\nColumns in 'ListeFour' table:")
    for column in columns:
        print(column)

    cursor.execute("PRAGMA table_info('Products');")
    columns = cursor.fetchall()
    print("\nColumns in 'Products' table:")
    for column in columns:
        print(column)

    cursor.execute("PRAGMA table_info('ProductPDFs');")
    columns = cursor.fetchall()
    print("\nColumns in 'ProductPDFs' table:")
    for column in columns:
        print(column)

    conn.close()

if __name__ == "__main__":
    db_path = get_db_path("cost_calculation.db")
    create_tables(db_path)
    alter_product_pdfs_table(db_path)
    populate_listefour(db_path)
    check_tables(db_path)
