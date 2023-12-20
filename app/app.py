#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import db, ma, Hero, Power, HeroPower
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)
ma.init_app(app)


class HeroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hero


class PowerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Power


class HeroPowerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HeroPower


hero_schema = HeroSchema()
power_schema = PowerSchema()
hero_power_schema = HeroPowerSchema()


# Helper function to get hero by ID
def get_hero_by_id(hero_id):
    hero = Hero.query.get(hero_id)
    if hero is None:
        abort(404, description="Hero not found")
    return hero


# Helper function to get power by ID
def get_power_by_id(power_id):
    power = Power.query.get(power_id)
    if power is None:
        abort(404, description="Power not found")
    return power


# Resource for /heroes
class HeroResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        result = hero_schema.dump(heroes, many=True)
        return jsonify(result)


# Resource for /heroes/<int:hero_id>
class HeroDetailResource(Resource):
    def get(self, hero_id):
        hero = get_hero_by_id(hero_id)
        result = hero_schema.dump(hero)
        return jsonify(result)


# Resource for /powers
class PowerResource(Resource):
    def get(self):
        powers = Power.query.all()
        result = power_schema.dump(powers, many=True)
        return jsonify(result)


# Resource for /powers/<int:power_id>
class PowerDetailResource(Resource):
    def get(self, power_id):
        power = get_power_by_id(power_id)
        result = power_schema.dump(power)
        return jsonify(result)

    def patch(self, power_id):
        power = get_power_by_id(power_id)
        new_description = request.json.get('description')

        if new_description:
            power.description = new_description

        try:
            db.session.commit()
            result = power_schema.dump(power)
            return jsonify(result)
        except ValueError as e:
            db.session.rollback()
            return jsonify({'errors': [str(e)]}), 400


# Resource for /hero_powers
class HeroPowerResource(Resource):
    def post(self):
        data = request.json
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')
        strength = data.get('strength')

        hero = get_hero_by_id(hero_id)
        power = get_power_by_id(power_id)

        new_hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=strength)

        try:
            db.session.add(new_hero_power)
            db.session.commit()
            result = hero_schema.dump(hero)
            return jsonify(result)
        except ValueError as e:
            db.session.rollback()
            
            # Check if the error is related to the 'description' validation
            if "Description must be at least 20 characters long" in str(e):
                return jsonify({'error': str(e)}), 400, {'Content-Type': 'application/json'}
            else:
                return jsonify({'error': 'Validation error'}), 400, {'Content-Type': 'application/json'}


# Add resources to the API
api.add_resource(HeroResource, '/heroes')
api.add_resource(HeroDetailResource, '/heroes/<int:hero_id>')
api.add_resource(PowerResource, '/powers')
api.add_resource(PowerDetailResource, '/powers/<int:power_id>')
api.add_resource(HeroPowerResource, '/hero_powers')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)