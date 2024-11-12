import sqlite3
import random
import string

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def populate_database():
    conn = sqlite3.connect('cost_calculation.db')
    cursor = conn.cursor()

    # Insert random products
    for _ in range(50):  # Number of products to insert
        code = random_string(6)
        nom_du_produit = random_string(10)
        fournisseur = random_string(8)
        unite = random.choice(['kg', 'pcs', 'litre'])
        colisage = random_string(5)
        devise = random.choice(['USD', 'EUR', 'TND'])
        prix_unitaire = round(random.uniform(10, 500), 2)
        volume = round(random.uniform(0.1, 100), 2)
        qte_par_palette = random.randint(10, 1000)
        conteneurs_20 = random.randint(1, 20)
        conteneurs_40 = random.randint(1, 10)
        autorisation = random_string(5)
        position_tarifaire = random_string(10)
        droits_taxes = random_string(5)
        eur1_on = random_string(5)
        incoterm = random_string(5)
        pelletisation = random_string(5)
        libre = random_string(5)
        convention_commerce = random_string(5)
        origine = random_string(5)
        timbre = round(random.uniform(0, 10), 2)
        total_exw = round(random.uniform(100, 1000), 2)
        total_charge_logistique = round(random.uniform(10, 100), 2)
        total_droits_et_taxes = round(random.uniform(10, 100), 2)
        total_frais = round(random.uniform(10, 100), 2)
        assurance = round(random.uniform(10, 100), 2)
        dd = round(random.uniform(10, 100), 2)
        fodec = round(random.uniform(10, 100), 2)
        tpe = round(random.uniform(10, 100), 2)
        tva = round(random.uniform(10, 100), 2)
        rdp = round(random.uniform(10, 100), 2)
        air = round(random.uniform(10, 100), 2)
        anged = round(random.uniform(10, 100), 2)
        fret = round(random.uniform(10, 100), 2)
        fret_davis_darrivee = round(random.uniform(10, 100), 2)
        uc = round(random.uniform(10, 100), 2)
        magasinage = round(random.uniform(10, 100), 2)
        manutention = round(random.uniform(10, 100), 2)
        transport_local = round(random.uniform(10, 100), 2)
        honoraire_de_transitaire = round(random.uniform(10, 100), 2)
        cost_price = round(random.uniform(100, 1000), 2)

        cursor.execute('''
        INSERT INTO Products (code, nom_du_produit, fournisseur, unite, colisage, devise, prix_unitaire, volume, qte_par_palette, 
                              conteneurs_20, conteneurs_40, autorisation, position_tarifaire, droits_taxes, eur1_on, incoterm, 
                              pelletisation, libre, convention_commerce, origine, timbre, total_exw, total_charge_logistique, 
                              total_droits_et_taxes, total_frais, assurance, dd, fodec, tpe, tva, rdp, air, anged, fret, 
                              fret_davis_darrivee, uc, magasinage, manutention, transport_local, honoraire_de_transitaire, cost_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (code, nom_du_produit, fournisseur, unite, colisage, devise, prix_unitaire, volume, qte_par_palette, conteneurs_20,
              conteneurs_40, autorisation, position_tarifaire, droits_taxes, eur1_on, incoterm, pelletisation, libre, convention_commerce,
              origine, timbre, total_exw, total_charge_logistique, total_droits_et_taxes, total_frais, assurance, dd, fodec, tpe, tva,
              rdp, air, anged, fret, fret_davis_darrivee, uc, magasinage, manutention, transport_local, honoraire_de_transitaire, cost_price))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_database()
