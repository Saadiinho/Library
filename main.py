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


def create_user(conn):
    cursor = conn.cursor()
    query = """SELECT COUNT(*) FROM `user`"""
    cursor.execute(query)
    result = cursor.fetchone()
    first_name = input("Prénom : ")
    last_name = input("Nom : ")
    year = int(input("Age : "))
    email = input("Mail : ")
    user = us.User(id_user=result, first_name=first_name, last_name=last_name, year=year, email=email)
    return user


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
        user = us.User(id_user, first_name, result[2], result[4], result[3])
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
                    user.consult_book(conn) 
                elif action == 2:
                    user.search_book(conn) 
                elif action == 3:
                    user.read_copy(conn) 
                elif action == 4:
                    user.search_copy_specific(conn) 
                elif action == 5:
                    user.my_book(conn) 
                elif action == 6:
                    user.loan(conn)     
                elif action == 7:
                    user.return_book(conn)
                else :
                    print("Merci de votre visite et à bientôt", result[1], "!")
                    return
            else :
                print("Vous êtes passé en mode administrateur")
                return

    else:
        print("L'utilisateur n'existe pas encore. Veuillez vous inscrire.\nInscription\n")
        new_user = create_user(conn)
        new_user.create_user(conn)
    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()

if __name__ == "__main__":
   conn = connect_db()
   connection(conn)
   conn.close()


