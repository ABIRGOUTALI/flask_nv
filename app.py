from flask import Flask, request, jsonify
import json
import pymysql


# Creation of an instance named app
app = Flask(__name__)

#creation d'une connection a la base de donnees  books.sqlite
def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='flask_db',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
            #spécifie que PyMySQL doit utiliser un curseur qui renvoie les résultats des requêtes sous forme de dictionnaires Python,
            # ce qui permet d'accéder aux données de la base de données par leur nom plutôt que par leur index. 
            #Cela rend la manipulation des données plus facile et plus intuitive.
        )
    except pymysql.Error as e :
        print(e)
    return conn

@app.route('/')
def hello():
    return "Hello CODABI ❤️🙋‍♀️🙋‍♂️!"

# Get all books or add a new book
@app.route('/books', methods=['GET', 'POST'])
def books():
    #ajouter la connexion BD
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("SELECT * FROM book")
        books=[
            dict(id=row['id'],author=row['author'],language=row['language'],title=row['title'])
            for row in cursor.fetchall()
            ]

        if books is not None:
            return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO book (author, language, title) VALUES  (%s, %s, %s)"""
        #question marks are used to protect against SQL injection attacks
        #the ? placeholders will be replaced by the  values provided in the execute statement below
        cursor.execute(sql, (new_author, new_lang, new_title))
        #commit changes and close the database connection
        conn.commit()
        #return success message with the id of the last inserted
        #ppour confirmer notre demande nous recuperons l'ID de ce objet  en utilisant l'attribut ID 
        #et retun comme une reponse
        return f" created successfully"

@app.route('/book/<int:id>',methods=['GET','PUT','DELETE'])
def single_books(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method =='GET':
        cursor.execute("SELECT * FROM book WHERE id=%s", (id,))
        row = cursor.fetchone()
        if row:
            book = {'id': row['id'], 'author': row['author'], 'language': row['language'], 'title': row['title']}
            return jsonify(book), 200
        else:
            return "Book not found ", 404
         
    if request.method =='PUT':
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        sql = """UPDATE book 
                 SET title=%s,
                 author=%s,
                 language=%s
                 WHERE id=%s"""
        cursor.execute(sql, (title, author, language, id))
        conn.commit()    
        updated_book = {'id': id, 'author': author, 'language': language, 'title': title}
        return  jsonify(updated_book)

    if request.method =='DELETE':
        sql= """DELETE FROM book WHERE id=%s"""
        cursor.execute(sql, (id,))  
        conn.commit()
        return f"The book with id {id} has been deleted 👾", 200


if __name__ == '__main__':
    app.run(debug=True)
