from .database import connect


def get_products():
    db = connect()

    if db is None:
        return []

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id_produktu,
            p.nazwa,
            p.opis,
            p.cena,
            p.ilosc,
            p.zdjecie,
            k.nazwa AS kategoria
        FROM produkty p
        JOIN kategorie k
        ON p.id_kategorii = k.id_kategorii
    """)

    products = cursor.fetchall()

    cursor.close()
    db.close()

    return products


if __name__ == "__main__":
    for product in get_products():
        print(product["nazwa"], product["cena"], "zl")
