from flask_restful import Resource
from models.storemodel import StoreModel


class Store(Resource):

    @staticmethod
    def get(name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @staticmethod
    def post(name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except ConnectionError:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    @staticmethod
    def delete(name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):

    @staticmethod
    def get():
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
