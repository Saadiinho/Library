import mysql.connector
import book as bk
import loan as ln
import user as us
import exemplaire as ex

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="library"
    )
    return conn


def read_bdd(conn, table, condition):
    cursor = conn.cursor()
    query = "SELECT * FROM " + table 
    if condition != "":
        query += f" WHERE {condition}"
    cursor.execute(query)
    books = cursor.fetchall()
    for book in books:
        print(f"{book[0]}: {book[1]}, {book[2]}, {book[3]}, {book[4]}")


def loan(conn, id_user, id_book):
    cursor = conn.cursor()
    # Check if the book is available
    cursor.execute("SELECT id_copy FROM copy WHERE id_book = %s AND status = 'Available'", (id_book,))
    result = cursor.fetchone()
    if result is None:
        print("Book not available")
        return False
    id_copy = result[0]
    # Set the copy status to 'Borrowed'
    cursor.execute("UPDATE copy SET status = 'Borrowed' WHERE id_copy = %s", (id_copy,))
    # Create a new loan
    cursor.execute("INSERT INTO loan (id_copy, id_user) VALUES (%s, %s)", (id_copy, id_user))
    # Commit the changes
    conn.commit()
    print("Book loaned successfully")
    return True



if __name__ == "__main__":
    conn = connect_db()
    
    #bk.create_book(conn, "Test Book1", "Test Author", "Romance", "Anglais")
    #bk.consult_book(conn)
    #bk.search_book(conn)
    #bk.update_book(conn, 4)
    #bk.delete_book(conn)

    #ex.create_copy(conn)
    ex.read_copy(conn)
    #ex.search_copy_specific(conn)
    
    #read_bdd(conn, "user", "")

    #us.create_user(conn)
    #us.connection(conn)
    conn.close()