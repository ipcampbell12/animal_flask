from multiprocessing import connection
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

    @classmethod
    def insert(cls,animal): 

        connection = sqlite3.connect("zoo.db")
        cursor = connection.cursor()

        query = '''
            INSERT INTO animals
            VALUES (?,?)
        '''

        cursor.execute(query,(animal['type'],animal['quantity']))
        connection.commit()
        connection.close()
    
    @classmethod
    def update(cls,animal): 

        connection = sqlite3.connect("zoo.db")
        cursor = connection.cursor()

        query = '''
            UPDATE animals
            SET quantity =?
            WHERE type =?
        '''

        cursor.execute(query,(animal['quantity'],animal['type']))
        connection.commit()
        connection.close()




    @jwt_required()
    def post(self, type):

        if self.find_by_type(type) is not None:
            return {'message': f'Animal with type {type} already exists'}, 400

        request_data = Animal.parser.parse_args()
        animal = {
            "type": type,
            "quantity": request_data["quantity"]
        }
        
        try: 
            self.insert(animal)
        except: 
            return {"Message":f"The animal {animal} could not be inserted"}

        return animal, 201

    @jwt_required()
    def delete(self,type):
        connection = sqlite3.connect('zoo.db')
        cursor = connection.cursor()

        query = '''
            DELETE FROM animals
            WHERE type = ?
        '''

        cursor.execute(query,(type,))
        connection.commit()
        connection.close()
        return {"Message":f"The animal {type} has been deleted "}


    @jwt_required()
    def put(self,type):
       
        request_data = Animal.parser.parse_args()
        animal = self.find_by_type(type)
        updated_animal = {'type':type,'quantity':request_data['quantity']}

        if animal is None:
            try: 
                self.insert(updated_animal)
            except: 
                return {"Message":f"An error ocurred when inserting {type}" }
        else:
            try: 
                animal.update(updated_animal)
            except: 
                return {"Message":f"An error ocurred when inserting {type}" }

        return updated_animal

# define animals resource


class AnimalList(Resource):
    def get(self):
        connection = sqlite3.connect('zoo.db')
        cursor = connection.cursor()

        query = '''
            SELECT * FROM animals
        '''
        result = cursor.execute(query)

        animals = []

        for row in result: 
            animals.append({'type':row[0],'quantity':row[1]})


        return {"animals": animals}