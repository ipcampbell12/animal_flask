import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Animal(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('quantity',
        type=int,
        required=True,
        help="Must include quantity"
        )

    @jwt_required()
    def get(self, type):
        animal =self.find_by_type(type)
        if animal is not None:
            return animal
        return {"message":"Item not found"}
        
    @classmethod
    def find_by_type(cls,type):

        connection = sqlite3.connect('zoo.db')
        cursor = connection.cursor()

        query = '''
            SELECT * FROM animals WHERE type = ?
        '''
        result = cursor.execute(query,(type,))

        row = result.fetchone()
        connection.close()

        if row is not None:
            return {"animal":{'type':row[0],'quantity':row[1]}}


    @jwt_required()
    def post(self, type):

        if self.find_by_type(type) is not None:
            return {'message': f'Animal with type {type} already exists'}, 400

        request_data = Animal.parser.parse_args()
        animal = {
            "type": type,
            "quantity": request_data["quantity"]
        }
        
        connection = sqlite3.connect("zoo.db")
        cursor = connection.cursor()

        query = '''
            INSERT INTO animals
            VALUES (?,?)
        '''

        cursor.execute(query,(animal['type'],animal['quantity']))
        connection.commit()
        connection.close()

        return animal, 201

    @jwt_required()
    def delete(self,type):
        global animals
        animals = list(filter(lambda x:x['type']!=type,animals))
        return {"Message":f"The animals {type} was removed. The {type} will be soarely missed."}

    @jwt_required()
    def put(self,type):
       
        request_data = Animal.parser.parse_args()
        animal = next(filter(lambda x:x['type']==type,animals),None)
        if animal is None:
            animal = {'type':type,'quantity':request_data['quantity']}
            animals.append(animal)
        else:
            animal.update(request_data)
        return animal

# define animals resource


class AnimalList(Resource):
    def get(self):
        return {"animals": animals}