#Fonction qui permet à l'utilisateur de se connecter
import book as bk
import exemplaire as ex


class User:
    def __init__(self, id_user: int, first_name: str, last_name: str, year: int, email: str):
        self.id_user = id_user
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.year = year

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
            query = "INSERT INTO user (first_name, last_name, email, years) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (self.first_name, self.last_name, self.email, self.year))
            conn.commit()
            print("Inscription réussie.")
        # Fermeture du curseur et de la connexion
        cursor.close()
        conn.close()

    def consult_book(self, conn):
        cursor = conn.cursor()
        query = "SELECT id_book, title AS Titre, author AS Auteur, genre FROM book"
        cursor.execute(query)
        books = cursor.fetchall()
        for book in books:
            print(book)

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
