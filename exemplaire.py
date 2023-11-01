import book as bk
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
def read_copy(conn):
    cursor = conn.cursor()
    query = """
            SELECT copy.id_copy AS "ID de l'exemplaire", book.title AS Titre, book.author AS Auteur, book.genre AS Genre, copy.state AS Etat, 
            copy.available AS Disponibilité, copy.langue AS Langue 
            FROM book 
            JOIN copy ON book.id_book = copy.id_book;
            """
    cursor.execute(query)
    copies = cursor.fetchall()
    for copy in copies:
        print(copy)

def search_copy_specific(conn):
    cursor = conn.cursor()
    title = input("Entrez le titre du livre que vous recherchez : ")
    query = """SELECT copy.id_copy AS "ID de l'exemplaire", book.title AS Titre, book.author AS Auteur, book.genre AS Genre, copy.state AS Etat, copy.available AS Disponibilité, copy.langue AS Langue FROM book JOIN copy ON book.id_book = copy.id_book WHERE book.title = """ '"' + title + '"  AND copy.available = 1'
    cursor.execute(query)
    copies = cursor.fetchall()
    for copy in copies:
        print(copy)