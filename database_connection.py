import mysql.connector

DB_USER="rootuser"
DB_PASSWORD="1234"
DB_DATABASE="chrome_extension"
DB_HOST="localhost"

def db_connector():
    print(">> Into the function of db connector")
    try:
        db = mysql.connector.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_DATABASE,
                host=DB_HOST
                )
        return {"db":db,"status":"success"}
    except Exception as err:
        print("ERROR : Error occured in the db connector function : ",err)
        return {"db":None,"status":"error"}

