import pymysql

#creation d'une connection 
#on va  utiliser la fct connect 
conn = pymysql.connect(
    host='localhost',
        user='root',
        password='',
        database='flask_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
)


#cursor object : utiliser pour executer les requettes SQL
cursor = conn.cursor()
# sql_query : pour creer  notre table 
sql_query = """ CREATE TABLE  book(
          id integer PRIMARY KEY,
          author text NOT NULL, 
          language text NOT NULL,
          title  text NOT NULL
)"""

cursor.execute(sql_query) #execution de la requette
#insertion des donnees dans la base
conn.close()