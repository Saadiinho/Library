import book as bk
import user as us


class Copy:
    def __init__(self, state: str, id_book: int, available: bool, langue: str):
        self.state = state
        self.id_book = id_book
        self.availbale = available
        self.langue = langue
        self.id_user = None

    def get_data(self):
        return self.__dict__
            
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


    #Update : Fonction qui permet à l'administrateur de modifier les exemplaires présents dans la base de données
    def update_copy(conn, self):
        cursor = conn.cursor()
        self.read_copy(conn)
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
    def delete_copy(conn, self):
        cursor = conn.cursor()
        self.read_copy(conn)
        try:
            id = int(input("Choisissez l'identifiant du livre que vous souhaitez supprimer : "))
        except ValueError:
            print("Erreur : Vous devez entrer un chiffre.")
            return
        query = "DELETE FROM `copy` WHERE `copy`.`id_copy` = " + str(id)
        cursor.execute(query)
        conn.commit()
        print(f"Livre avec l'id {id} supprimé avec succès.")

    

