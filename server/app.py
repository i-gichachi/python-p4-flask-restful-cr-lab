#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True
app.json_encoder = None

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.serialize() for plant in plants])

    def post(self):
        data = request.get_json()
        name = data.get('name')
        image = data.get('image', None)  # Allow image to be nullable
        price = data.get('price')
        if not name or price is None:
            return make_response(jsonify({"error": "Missing data"}), 400)

        plant = Plant(name=name, image=image, price=price)
        db.session.add(plant)
        db.session.commit()
        return jsonify(plant.serialize()), 201
    
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant is None:
            return make_response(jsonify({"error": "Plant not found"}), 404)
        return jsonify(plant.serialize())

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
