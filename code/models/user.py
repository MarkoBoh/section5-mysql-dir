import sqlite3
from types import coroutine
import mysql.connector
from models.utilities import fields, connection

class UserModel():
    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password
    
    def json_user(self):
        return {'username':self.username}

    @classmethod
    def find_by_username(cls,username):
        #connection = sqlite3.connect('data.db')
        connection= mysql.connector.connect(
            user = "marko",
            password ="marko123!!",
            host ="localhost",
            database = "api"
        )
        cursor = connection.cursor()
        query = "SELECT * FROM `users` WHERE `username` = %s"
        print(query)
        rs = cursor.execute(query,(username,)) #mora biti tuple type
        #print(var_dump(results))
        row = cursor.fetchone()
        fields_map = fields(cursor)
        if row is not None:
            # kot defirnirano v init razreda
            user = cls(row[fields_map['id']],row[fields_map['username']],row[fields_map['password']])  
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls,_id):   # metoda klase
        #connection = sqlite3.connect('data.db')
        connection = mysql.connector.connect(
            user = "marko",
            password ="marko123!!",
            host ="localhost",
            database = "api"
        )
        cursor = connection.cursor()
        
        query = "SELECT * FROM `users` WHERE `id` = %d" %  (_id)
        result = cursor.execute(query) 
        row = cursor.fetchone()

        if row is not None:
            user = cls(row[0],row[1],row[2])  # kot defirnirano v init razreda
            #user = cls(*row)  # kot defirnirano v init razreda
        else:
            user = None
        connection.close()
        return user

