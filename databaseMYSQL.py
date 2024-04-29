import mysql.connector

mydb = mysql.connector.connect(
    host="<hostname>",
    user="<username>",
    password="<password>",
    database="<databasename>"
)

mycursor = mydb.cursor()
