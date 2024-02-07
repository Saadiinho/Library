class User:
    #Constructeur qui permet de créer un nouvel utilisateur.
    def __init__(self, id_user: int, first_name: str, last_name: str, year: int, email: str, password: str):
        self.id_user = id_user
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.year = year
        self.password = password

    #Guetteur qui permet de retourner sous la forme d'un dictionnaire les informations de l'utilisateur
    def get_data(self):
        return self.__dict__
    def get_idUser(self):
        return self.id_user

#Fonction qui permet à l'utilisateur de s'inscrire
    def create_user(self, conn):
        #Vérification dans la base de données
        cursor = conn.cursor()
        # Vérification de l'existence de l'utilisateur dans la base de données
        query = "SELECT * FROM user WHERE first_name = '%s' AND last_name = '%s'" % (self.first_name, self.last_name)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            print("L'utilisateur existe déjà existe déjà. Veuillez vous connecter.")
        else:
            # Inscription de l'utilisateur
            query = "INSERT INTO user (first_name, last_name, email, years, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (self.first_name, self.last_name, self.email, self.year, self.password))
            conn.commit()
            print("Inscription réussie.")
        # Fermeture du curseur et de la connexion
        cursor.close()
        conn.close()

#Fonction qui permet de consulter tous les livres dans la base de données
    def consult_book(self, conn):
        cursor = conn.cursor()
        query = "SELECT id_book, title AS Titre, author AS Auteur, genre FROM book"
        cursor.execute(query)
        books = cursor.fetchall()
        for book in books:
            print(book)

#Fonction qui permet de rechercher un livre spécifique
    def search_book(self, conn):
        title = input("Entrez le titre du livre : (laissez vide si vous ne le connaissez pas) ")
        author = input("Entrez le nom de l'auteur : (laissez vide si vous ne le connaissez pas) ")
        genre = input("Entrez le genre : (laissez vide si vous n'en avez pas) ")
        print('\n')
        cursor = conn.cursor()
        sql_query = """SELECT * FROM book WHERE 
                    (title LIKE %s OR %s = '') AND
                    (author LIKE %s OR %s = '') AND
                    (genre LIKE %s OR %s = '')"""
        cursor.execute(sql_query, ('%' + title + '%', title, '%' + author + '%', author, '%' + genre + '%', genre))

        results = cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("Aucun livre trouvé correspondant à ces critères.")

#Fonction qui permet de voir tous les copies de tous les livres présents et disponible dans la base de données
    def read_copy(self, conn):
        cursor = conn.cursor()
        query = """
                SELECT copy.id_copy AS "ID de l'exemplaire", book.title AS Titre, book.author AS Auteur, book.genre AS Genre, copy.state AS Etat, 
                copy.langue AS Langue 
                FROM book 
                JOIN copy ON book.id_book = copy.id_book
                WHERE copy.available = 1
                """
        cursor.execute(query)
        copies = cursor.fetchall()
        for copy in copies:
            print(copy)

#Fonction qui permet de chercher un exemplaire précis dans la base de données
    def search_copy_specific(self, conn):
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

#Fonction qui permet de consulter les livre empruntés par l'utilisateur
    def my_book(self, conn): 
        id_user = self.id_user
        cursor = conn.cursor()
        query = """
                    SELECT copy.id_copy AS Identifiant, 
                    book.title AS Titre, book.author AS Auteur, 
                    book.genre AS Genre, copy.state AS Etat, copy.langue AS Langue 
                    FROM copy
                    JOIN book ON copy.id_book = book.id_book
                    WHERE copy.id_user = """+ str(id_user) + """
                """
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("Vous n'avez empruntés aucun livre.")

#Fonction qui permet d'emprunter un exemplaire d'un livre
    def loan(self, conn):
        id_user = self.id_user
        cursor = conn.cursor()
        self.read_copy(conn)
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
    
#Fonction qui permet de retourner un livre une fois l'emprunt terminé
    def return_book(self, conn):
        id_user = self.id_user
        cursor = conn.cursor()
        self.my_book(conn)
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

#Fonction qui permet à l'administrateur de supprimer un livre dans la base de données
    def delete_book(self, conn):
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
        print(f"Livre avec l'id {id} supprimé avec succès.\n")
        
#fonction qui permet à l'administrateur de modifier un livre présent dans la base de données
    def update_book(self, conn):
        cursor = conn.cursor()
        self.consult_book(conn)
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

#Fonction qui permet d'ajouter un exemplaire d'un livre dans la base de données
    def create_copy(self, conn):
        cursor = conn.cursor()
        self.consult_book(conn)
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

#Fonction qui permet de modifier un exemplaire d'un livre
    def update_copy(self, conn):
        cursor = conn.cursor()
        self.read_copy(conn)
        try:
            id = int(input("Entrez l'id de l'exemplaire que vous souhaitez modifié : (Les id sont rangé par ordre croissant) "))
        except ValueError:
            print("Erreur : Vous devez entrer un chiffre.")
            return
        query = "SELECT * FROM `copy` WHERE id_copy =" + str(id)
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

#Fonction qui permet de supprimer un exemplaire d'un livre
    def delete_copy(self, conn):
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

#Fonction qui permet de supprimer un utilisateur
    def delete_user(self, conn):
        cursor = conn.cursor()
        query = "SELECT id_user, first_name AS Prenom, last_name AS Nom, email FROM user"
        cursor.execute(query)
        books = cursor.fetchall()
        for book in books:
            print(book)
        try:
            id = int(input("Choisissez l'identifiant du l'utilisateur que vous souhaitez supprimer : "))
        except ValueError:
            print("Erreur : Vous devez entrer un chiffre.")
            return
        query = "DELETE FROM `user` WHERE `user`.`id_user` = " + str(id)
        cursor.execute(query)
        conn.commit()
        print(f"L'utilisateur avec l'id {id} supprimé avec succès.")