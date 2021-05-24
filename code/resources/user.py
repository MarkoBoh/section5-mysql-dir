from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import UserModel
import mysql.connector
from models.utilities import fields

class UserRegister(Resource): # ker rabimo endpoint mora biti drugi razred
    parser = reqparse.RequestParser()
    parser.add_argument('username',    # ce ostalih argumentov ne navedemo, ne bodo sprejeti!!!
        type=str,
        required=True,
        help="To polje ne more biti prazno"
    )
    parser.add_argument('password',    # ce ostalih argumentov ne navedemo, ne bodo sprejeti!!!
        type=str,
        required=True,
        help="To polje ne more biti prazno"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {"message": "User exists"},400

        #connection = sqlite3.connect('data.db')
        connection= mysql.connector.connect(
            user = "marko",
            password ="marko123!!",
            host ="localhost",
            database = "api"
        )
        
        cursor = connection.cursor()
        # INSERT INTO `users`(`id`, `username`, `password`) VALUES (1,'demouser','dolgo geslo')
        password_hash = generate_password_hash(data['password'])
        query = "INSERT INTO users (`id`, `username`, `password`) VALUES (NULL,'"+ data['username'] + "','" + password_hash +"')"
        
        print(query)
       
        cursor.execute(query)
        connection.commit()
        connection.close()
        return data['username'],200

class Users(Resource):
    def get(self):
        #connection = sqlite3.connect('data.db')
        connection= mysql.connector.connect(
            user = "marko",
            password ="marko123!!",
            host ="localhost",
            database = "api"
        )
        cursor = connection.cursor()

        query = "SELECT * FROM `users` "
        #print(query)
        rs = cursor.execute(query)
        result = cursor.fetchall()
        fields_map = fields(cursor)
      
        if result is not None:
            seznam =[]
            for row in result:
                seznam.append({'username':row[fields_map['username']],'password':row[fields_map['password']]})
            return seznam, 200
       
        connection.close()
        return {"message":"Prazen seznam"}, 200 


