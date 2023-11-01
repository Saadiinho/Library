import book as bk
import user as us
#Create : Fonction qui permet à l'administrateur d'ajouter de nouveaux exemplaires d'un livre à la base de données
def create_copy(conn):
    cursor = conn.cursor()
    bk.search_book(conn)
    try:
        id_book = int(input("Entrez l'id du livre que vous souhaitez : "))
    except ValueError:
        print("Erreur : Vous devez entrer un chiffre.")
        return
    state = input("L'état de l'exemplaire : ")
    if not state in ["Neuf", "Bon", "Moyen", "Mauvais"]:
        print("Erreur : L'état doit être 'Neuf', 'Bon', 'Moyen' ou 'Mauvais'.")
        return
    available = int(input("1 s'il est disponible, 0 sinon : "))
    if available != 0 and available != 1:
        print("Erreur : Vous devez saisir 0 ou 1.")
        return
    langue = input("Entrez la langue de l'exemplaire : ")
    if not langue in ["Français", "Anglais"]:
        print("La bibliothèque ne stocke pas des livres d'autre langue que le français ou l'anglais")
        return
    query = """
            INSERT INTO copy (id_book, state, available, langue)
            VALUES
            (%s, %s, %s, %s)
            """
    cursor.execute(query, (id_book, state, available, langue))
    conn.commit()
    print(f"Exemplaire ajouté avec succès.")


#Read : Fonction qui permet à l'utilisateur de consulter tous les exemplaires de la base de données
def read_copy(conn, condition):
    cursor = conn.cursor()
    query = """
            SELECT copy.id_copy AS "ID de l'exemplaire", book.title AS Titre, book.author AS Auteur, book.genre AS Genre, copy.state AS Etat, 
            copy.langue AS Langue 
            FROM book 
            JOIN copy ON book.id_book = copy.id_book
            """ + condition
    cursor.execute(query)
    copies = cursor.fetchall()
    for copy in copies:
        print(copy)

def search_copy_specific(conn):
    cursor = conn.cursor()
    title = input("Entrez le titre du livre que vous recherchez : ")
    query = """SELECT copy.id_copy AS "ID de l'exemplaire", book.title AS Titre, book.author AS Auteur, book.genre AS Genre, copy.state AS Etat, copy.langue AS Langue FROM book JOIN copy ON book.id_book = copy.id_book WHERE book.title = """ '"' + title + '"  AND copy.available = 1'
    cursor.execute(query)
    copies = cursor.fetchall()
    if copies :
        for copy in copies:
            print(copy)
    else :
        print("Aucun exemplaire n'a été trouvé pour ce livre.")

#Update : Fonction qui permet à l'administrateur de modifier les exemplaires présents dans la base de données
def update_copy(conn):
    cursor = conn.cursor()
    read_copy(conn)
    try:
        id = int(input("Entrez l'id de l'exemplaire que vous souhaitez modifié : (Les id sont rangé par ordre croissant) "))
    except ValueError:
        print("Erreur : Vous devez entrer un chiffre.")
        return
    query = "SELECT * FROM `copy` WHERE id_copy =" + str(id)
    print(query)
    cursor.execute(query)
    copies = cursor.fetchall()
    for copy in copies:
        print(copy)
    state = input(f"L'état de l'exemplaire : ('{copy[2]}' si l'état ne change pas) ")
    if not state in ["Neuf", "Bon", "Moyen", "Mauvais"]:
        print("Erreur : L'état doit être 'Neuf', 'Bon', 'Moyen' ou 'Mauvais'.")
        return
    langue = input(f"Entrez la langue de l'exemplaire : ('{copy[4]}' si la langue ne change pas)")
    if not langue in ["Français", "Anglais", ""]:
        print("La bibliothèque ne stocke pas des livres d'autre langue que le français ou l'anglais")
        return
    query = "UPDATE copy SET state = %s, langue = %s WHERE id_copy = %s"
    cursor.execute(query, (state, langue, id))
    conn.commit()
    print(f"Livre avec l'id {id} mise à jour avec succès.")

#Delete : Fonction qui permet à l'administrateur de supprimer les exemplaires présents dans la base de données
def delete_copy(conn):
    cursor = conn.cursor()
    read_copy(conn)
    try:
        id = int(input("Choisissez l'identifiant du livre que vous souhaitez supprimer : "))
    except ValueError:
        print("Erreur : Vous devez entrer un chiffre.")
        return
    query = "DELETE FROM `copy` WHERE `copy`.`id_copy` = " + str(id)
    cursor.execute(query)
    conn.commit()
    print(f"Livre avec l'id {id} supprimé avec succès.")

def loan(conn, id_user):
    cursor = conn.cursor()
    read_copy(conn, "WHERE available = 1;")
    try:
        id_copy = int(input("Entrez l'id du livre que vous souhaitez emprunté : "))
    except ValueError:
        print("Erreur : Vous devez entrer un chiffre.")
        return
    query = f"""
            UPDATE copy SET id_user = {id_user}, available = 0 WHERE id_copy = {id_copy}
            """
    cursor.execute(query)
    conn.commit()
    print(f"Le livre a bien été prêté au lecteur n°{id_user}.")

def return_book(conn, id_user):
    cursor = conn.cursor()
    us.my_book(conn, id_user)
    try:
        id_copy = int(input("Entrez l'id du livre que vous souhaitez emprunté : "))
    except ValueError:
        print("Erreur : Vous devez entrer un chiffre.")
        return
    query = f"""
            UPDATE copy SET id_user = NULL, available = 1 WHERE id_copy = {id_copy}
            """
    cursor.execute(query)
    conn.commit()
    print(f"Le livre a bien été retourné par le lecteur n°{id_user}.")