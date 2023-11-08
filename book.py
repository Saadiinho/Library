class Book:
    def __init__(self, title: str, author: str, genre: str):
        self.title = title
        self.author = author
        self.genre = genre

    def get_data(self):
        return self.__dict__

    #Create : Fonction qui permet à l'administrateur d'ajouter un livre dans la base de données
    def create_book(conn, title, author, genre):
        cursor = conn.cursor()
        query = "INSERT INTO book (title, author, genre) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (title, author, genre))
        conn.commit()
        print(f"Livre '{title}' ajouté avec succès.")


    #Update : Fonction qui permet à l'administrateur de mettre à jour les données d'un livre dans la base de données
    def update_book(conn):
        cursor = conn.cursor()
        try:
            id = int(input("Entrez l'id du livre que vous souhaitez modifié : "))
        except ValueError:
            print("Erreur : Vous devez entrer un chiffre.")
            return
        query = "SELECT * FROM book WHERE id_book = " + str(id)
        cursor.execute(query)
        books = cursor.fetchall()
        for book in books :
            print(book)
        title = input(f"Entrez le nouveau titre : ('{book[1]}' si le nom ne change pas) ")
        author = input(f"Entrez le nouvel auteur : ('{book[2]}' s'il n'y en a pas) ")
        genre = input(f"Entrez le nouveau genre : ('{book[3]}' s'il n'y en a pas) ")
        query = "UPDATE book SET title = %s, author = %s, genre = %s WHERE id_book = %s"
        cursor.execute(query, (title, author, genre, id))
        conn.commit()
        print(f"Livre avec l'id {id} mise à jour avec succès.")

    #Delete : Fonction qui permet à l'administrateur de supprimer un livre
    def delete_book(conn, self):
        cursor = conn.cursor()
        self.consult_book(conn)
        try:
            id = int(input("Choisissez l'identifiant du livre que vous souhaitez supprimer : "))
        except ValueError:
            print("Erreur : Vous devez entrer un chiffre.")
            return
        query = "DELETE FROM `book` WHERE `book`.`id_book` = " + str(id)
        cursor.execute(query)
        conn.commit()
        print(f"Livre avec l'id {id} supprimé avec succès.")

