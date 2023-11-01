import mysql.connector
import book as bk
import user as us
import exemplaire as ex

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="library"
    )
    return conn


def read_bdd(conn, table, condition):
    cursor = conn.cursor()
    query = "SELECT * FROM " + table 
    if condition != "":
        query += f" WHERE {condition}"
    cursor.execute(query)
    books = cursor.fetchall()
    for book in books:
        print(f"{book[0]}: {book[1]}, {book[2]}, {book[3]}, {book[4]}")


def connection(conn):
    first_name = input("Entrez votre prénom :")
    last_name = input("Entrez votre nom de famille :")
    cursor = conn.cursor()
    query = "SELECT * FROM user WHERE first_name = '%s' AND last_name = '%s'" % (first_name, last_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        id_user = result[0]
        first_name = result[1]
        print("Bienvenue", first_name, "!")
        while True:
            if id_user != 1:
                action = int(input("\nQue voulez-vous faire ?\n" \
                                "\t1 - Consulter les livres\n"\
                                "\t2 - Rechercher un livre\n"\
                                "\t3 - Consulter tous les exemplaires disponible\n"\
                                "\t4 - Consulter les exemplaires d'un livre en particulier\n"\
                                "\t5 - Consulter vos livres empruntés\n"\
                                "\t6 - Emprunter un livre\n"\
                                "\t7 - Retourner un livre\n"\
                                "\t0 - Se déconnecter\n"))
                if action == 1:
                    print("\nVoici la liste des livres présents dans la bibliothèque :")
                    bk.consult_book(conn)
                elif action == 2:
                    bk.search_book(conn)
                elif action == 3:
                    ex.read_copy(conn)
                elif action == 4:
                    ex.search_copy_specific(conn)
                elif action == 5:
                    us.my_book(conn, id_user)
                elif action == 6:
                    ex.loan(conn, id_user)
                elif action == 7:
                    ex.return_book(conn, id_user)
                else :
                    print("Merci de votre visite et à bientôt", result[1], "!")
                    return
            else :
                print("Vous êtes passé en mode administrateur")
                return

    else:
        print("L'utilisateur n'existe pas encore. Veuillez vous inscrire.")
        us.create_user(conn)
        connection(conn)
    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()



if __name__ == "__main__":
    conn = connect_db()
    
    #bk.create_book(conn, "Test Book1", "Test Author", "Romance", "Anglais")
    #bk.consult_book(conn)
    #bk.search_book(conn)
    #bk.update_book(conn)
    #bk.delete_book(conn)

    #ex.create_copy(conn)
    #ex.read_copy(conn)
    #ex.update_copy(conn)
    #ex.delete_copy(conn)

    #read_bdd(conn, "user", "")

    #us.create_user(conn)
    connection(conn)
    conn.close()