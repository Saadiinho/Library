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
    


    

    #Delete : Fonction qui permet à l'administrateur de supprimer les exemplaires présents dans la base de données
   

    

