import sqlite3

def get_db_connection():
    conn = sqlite3.connect('cost_calculation.db')
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        name TEXT,
        unit TEXT,
        packaging TEXT,
        currency TEXT,
        exchange_rate REAL,
        unit_price REAL,
        quantity INTEGER,
        volume REAL,
        weight REAL,
        incoterm TEXT,
        authorization TEXT,
        commerce_convention TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        name TEXT,
        address TEXT,
        factory_address TEXT,
        currency TEXT,
        payment_terms TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Logistics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        freight REAL,
        arrival_notice_fee REAL,
        storage REAL,
        handling REAL,
        local_transport REAL,
        customs_agent_fee REAL,
        FOREIGN KEY (product_id) REFERENCES Products (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Taxes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        insurance REAL,
        dd REAL,
        fodec REAL,
        tpe REAL,
        tva REAL,
        rpd REAL,
        stamp REAL,
        air REAL,
        timbre REAL,
        FOREIGN KEY (product_id) REFERENCES Products (id)
    )
    ''')

    conn.commit()
    conn.close()
