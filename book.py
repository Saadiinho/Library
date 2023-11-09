class Book:
    def __init__(self, title: str, author: str, genre: str):
        self.title = title
        self.author = author
        self.genre = genre

    def get_data(self):
        return self.__dict__

    #Create : Fonction qui permet à l'administrateur d'ajouter un livre dans la base de données
    def create_book(self, conn):
        cursor = conn.cursor()
        query = "INSERT INTO book (title, author, genre) VALUES (%s, %s, %s)"
        cursor.execute(query, (self.title, self.author, self.genre))
        conn.commit()
        print(f"Livre '{self.title}' ajouté avec succès.")
