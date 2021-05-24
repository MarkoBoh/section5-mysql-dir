from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import mysql.connector
from models.utilities import fields

class Item(Resource):
    # parser je sedaj del razreda, ne metode, da nimamo duplicirane kode
    parser = reqparse.RequestParser()
    parser.add_argument('price',    # ce ostalih argumentov ne navedemo, ne bodo sprejeti!!!
        type=float,
        required=True,
        help="To polje ne more biti prazno"
    )

    @jwt_required()
    def get(self, name):  #name of the item
        item = ItemModel.find_by_name(name)
        if item:
            return item.json_item()
        return {'message': 'Item not found'}, 404

    
    def post(self, name):  ## moramo imeti enako strukturo
        # error first approch
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': "An item with name '{}' already exists.".format(name)},400

        data = Item.parser.parse_args()
        print(name)
        print(data)
        item = ItemModel(name, data['price'])
     
        try:
            item.insert_item()  #vrednosti so ze v item objektu
        except:
            return {"message":"Can't insert the item."}, 500
        
        return item.json_item(), 201 # Created OK!  202 is accepted when delaying creation
    
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            #connection = sqlite3.connect('data.db')
            connection= mysql.connector.connect(
                user = "marko",
                password ="marko123!!",
                host ="localhost",
                database = "api"
            )

            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name = '%s'" % (name)
            result = cursor.execute(query)
            connection.commit()
            connection.close()
            return {'message': 'Item deleted'}
        return {'message': 'Item does not exists'}

    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name) # trenutni item, ki ga najde ali pa ne v bazi
        updated_item = ItemModel(name, data['price']) #nova cena za item
        if item is None:
            try:
                updated_item.insert_item()
            except:
                return {"message":"Insert into items failed"}, 500 #internal server error
        else:
            try:
                updated_item.update_item() 
            except:
                return {"message":"update into items failed"}, 500 #internal server error
        return updated_item.json_item()

    

class ItemList(Resource):
    def get(self):
        #connection = sqlite3.connect('data.db')
        connection= mysql.connector.connect(
            user = "marko",
            password ="marko123!!",
            host ="localhost",
            database = "api"
        )

        cursor = connection.cursor()
        query = "SELECT * FROM `items`"
        cursor.execute(query)
        
        result = cursor.fetchall()
        field_map = fields(cursor) # da lahko stolpce klicemo po imenih, ne po zaporednih stevilkah
        seznam =[]
        if result is not None:
            for row in result:
                seznam.append({'name': row[field_map['name']],'price':row[field_map['price']]})
        
        connection.commit()
        connection.close()
        return seznam, 200