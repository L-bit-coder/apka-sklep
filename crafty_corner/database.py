import mysql.connector


def connect():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crafty_corner",
            port=3306,
        )

        print("Polaczono z baza danych!")
        return db

    except mysql.connector.Error as error:
        print("Blad polaczenia:", error)
        return None


if __name__ == "__main__":
    db = connect()

    if db:
        db.close()
