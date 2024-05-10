import pymysql

def createAccount(cursor,username,password):
    cursor.execute("")

def connect(func,host="localhost",user="root",password=""):
    connection=pymysql.connect(host=host,user=user,password=password)
    cursor=connection.cursor()

    func()
    cursor.execute("SHOW DATABASES;")
    output=cursor.fetchall()
    print(output)

    connection.close()