#Fonction qui permet à l'utilisateur de se connecter
def connection(conn):
    first_name = input("Entrez votre prénom :")
    last_name = input("Entrez votre nom de famille :")
    cursor = conn.cursor()
    query = "SELECT * FROM user WHERE first_name = '%s' AND last_name = '%s'" % (first_name, last_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        print("Connexion réussie.")
    else:
        print("L'utilisateur n'existe pas encore. Veuillez vous inscrire.")
    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()


#Fonction qui permet à l'utilisateur de s'inscrire
def create_user(conn):
    first_name = input("Entrez votre prénom :")
    last_name = input("Entrez votre nom de famille :")
    email = input("Entrez votre adresse mail :")
    year = int(input("Entrez votre âge :"))
    #Vérification dans la base de données
    cursor = conn.cursor()
    # Vérification de l'existence de l'utilisateur dans la base de données
    query = "SELECT * FROM user WHERE first_name = '%s' AND last_name = '%s'" % (first_name, last_name)
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        print("L'utilisateur existe déjà existe déjà. Veuillez vous connecter.")
    else:
        # Inscription de l'utilisateur
        query = "INSERT INTO user (first_name, last_name, email, years) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (first_name, last_name, email, year))
        conn.commit()
        print("Inscription réussie.")
    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()

#Fonction qui permet à l'utilisateur de recherher un livre spécifique avec un ou plusieurs filtres dans la base de données


#Fonction qui permet à l'utilisateur d'emprunter un livre

#Fonction qui permet à l'utilisateur de rendre un livre