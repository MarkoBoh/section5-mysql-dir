import sqlite3
import mysql.connector
from models.utilities import fields

# to potrebujemo, da lahko v rezultatu row klicemo po imenu stolpca, row[field_map['name']], namesto row[1]


class ItemModel():
    def __init__(self,name, price):
        self.name = name
        self.price = price

    def json_item(self):
        return {'name':self.name, 'price':self.price}

   
    @classmethod
    def find_by_name(cls,name):                     # tukja se nanasa na class
        #connection = sqlite3.connect('data.db')

        connection= mysql.connector.connect(
            user = "marko",
            password ="marko123!!",
            host ="localhost",
            database = "api"
        )

        cursor = connection.cursor()
        query = "SELECT * FROM `items` WHERE `name` ='%s'" % (name)
        rs = cursor.execute(query) 
        row = cursor.fetchone()
        connection.close()
        
        # imena stolcev v tabeli
        field_names = [i[0] for i in cursor.description]
        print(field_names)

        field_map = fields(cursor)
        """ print(row[field_map['name']])
        print(row[field_map['price']])
         """
        if row:
            return (cls( row[field_map['name']], row[field_map['price']]) ) 
        return None

   
    def insert_item(self): # v item imamo sedaj vrednosti!!!
        #connection = sqlite3.connect('data.db')
        connection= mysql.connector.connect(
            user = "marko",
            password ="marko123!!",
            host ="localhost",
            database = "api"
        )
        cursor = connection.cursor()
        print("prej 0 ")
        query = "INSERT INTO `items` VALUES (NULL,'%s',%f)" % (self.name, self.price)
        print(query)
        cursor.execute(query)

        connection.commit()
        connection.close()

    def update_item(self):
        #connection = sqlite3.connect('data.db')
        connection= mysql.connector.connect(
            user = "marko",
            password ="marko123!!",
            host ="localhost",
            database = "api"
        )

        cursor = connection.cursor()
        query = "UPDATE items SET price = %f WHERE name = '%s'" %  (self.price, self.name)
        print(query)

        cursor.execute(query)
        connection.commit()
        connection.close()
        return {'message': 'Item Updated'}