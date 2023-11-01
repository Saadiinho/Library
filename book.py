#Create : Fonction qui permet à l'administrateur d'ajouter un livre dans la base de données
def create_book(conn, title, author, genre):
    cursor = conn.cursor()
    query = "INSERT INTO book (title, author, genre) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (title, author, genre))
    conn.commit()
    print(f"Livre '{title}' ajouté avec succès.")


#Read : Fonction qui permet à l'utilisateur de consulter la liste de tous les livres présents dans la base de données
def consult_book(conn):
    cursor = conn.cursor()
    query = "SELECT id_book, title AS Titre, author AS Auteur, genre FROM book"
    cursor.execute(query)
    books = cursor.fetchall()
    for book in books:
        print(book)

def search_book(conn):
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
def delete_book(conn):
    cursor = conn.cursor()
    consult_book(conn)
    try:
        id = int(input("Choisissez l'identifiant du livre que vous souhaitez supprimer : "))
    except ValueError:
        print("Erreur : Vous devez entrer un chiffre.")
        return
    query = "DELETE FROM `book` WHERE `book`.`id_book` = " + str(id)
    cursor.execute(query)
    conn.commit()
    print(f"Livre avec l'id {id} supprimé avec succès.")
