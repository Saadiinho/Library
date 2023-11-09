import mysql.connector
import book as bk
import user as us
from getpass import getpass


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

def create_book(conn):
    cursor = conn.cursor()
    #Saisie des informations du livre dans la base de données
    title = input("Titre : ")
    author = input("Auteur : ")
    genre = input("Genre : ")
    #Vérification du livre dans la base de données
    sql_query = """SELECT * FROM book WHERE 
                    (title LIKE %s OR %s = '') AND
                    (author LIKE %s OR %s = '') AND
                    (genre LIKE %s OR %s = '')"""
    cursor.execute(sql_query, ('%' + title + '%', title, '%' + author + '%', author, '%' + genre + '%', genre))
    results = cursor.fetchall()
    if results:
        print("Le livre existe déjà dans la base de donnée.")
        return
        
    else:
        book = bk.Book(title=title, author=author, genre=genre)
        book.create_book(conn)


def connection(conn):
    first_name = input("Entrez votre prénom :")
    last_name = input("Entrez votre nom de famille :")
    password = getpass()
    cursor = conn.cursor()
    query = "SELECT * FROM user WHERE first_name = '%s'" % (first_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        id_user = result[0]
        first_name = result[1]
        if password == result[5]:
            print("Bienvenue", first_name, "!")
            user = us.User(id_user, first_name, result[2], result[4], result[3], password=password)
            while True:
                if id_user == 1:
                    choice = int(input(
                                    "\t1- Passage mode normal\n"\
                                    "\t2- Mode administrateur\n"\
                                    "\t0- Quitter\n"))
                if id_user != 1 or choice == 1:
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
                elif choice == 2 :
                    print("Vous êtes passé en mode administrateur")
                    
                    action = int(input("\nQue voulez-vous faire ?\n" \
                                    "\t1 - Ajouter un nouveau livre\n"\
                                    "\t2 - Supprimer un livre\n"\
                                    "\t3 - Modifier un livre\n"\
                                    "\t4 - Ajouter un exemplaire d'un livre\n"\
                                    "\t5 - Modifier un exemplaire d'un livre\n"\
                                    "\t6 - Supprimer l'exemplaire d'un livre\n"\
                                    "\t7 - Supprimer un utilisateur\n"\
                                    "\t0 - Se déconnecter\n"))
                    if action == 1:
                        create_book(conn) 
                    elif action == 2:
                        user.delete_book(conn) 
                    elif action == 3:
                        user.update_book(conn) 
                    elif action == 4:
                        user.create_copy(conn) 
                    elif action == 5:
                        user.update_copy(conn) 
                    elif action == 6:
                        user.delete_copy(conn)     
                    elif action == 7:
                        user.delete_user(conn)
                    else :
                        print("Merci de votre visite et à bientôt", result[1], "!")
                        return
                else : 
                    return
        else:
            print("Mot de passe incorrect.")
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


