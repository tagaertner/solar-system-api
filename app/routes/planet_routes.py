from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.planet import Planet

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    name = request_body["name"]
    moon= request_body["moon"]
    description = request_body["description"]

    new_planet = Planet(name=name, moon=moon, description=description)
    db.session.add(new_planet)
    db.session.commit()
    response = new_planet.to_dict()
    return response, 201

@planets_bp.get("")
def get_all_planets():
    description_param = request.args.get("description")
    moon_param = request.args.get("moon")
    moon_op_param = request.args.get("moon_param")
    sort_param = request.args.get("sort")
    
    query = db.select(Planet)   

    if description_param:
        query = query.where(Planet.description.like(f"%{description_param}%"))

    if moon_param:
        try:
            moon_count = int(moon_param)
            # Dictionary of comparison operators
            moon_operators = {
                "eq": Planet.moon.__eq__,
                "gt": Planet.moon.__gt__,
                "lt": Planet.moon.__lt__,
                "gte": Planet.moon.__ge__,
                "lte": Planet.moon.__le__
            }
            operator_func = moon_operators.get(moon_op_param, Planet.moon.__eq__)
            if operator_func:
                query = query.where(operator_func(moon_count))
        except ValueError:
            return {"message": "Invalid moon parameter"}, 400
  
    sort_options ={
        "name": Planet.name,
        "name_desc": Planet.name.desc(),
        "moon": Planet.moon,
        "moon_desc": Planet.moon.desc(),
        "id": Planet.id
    }    
    
    sort_field = sort_options.get(sort_param, Planet.id)
    query = query.order_by(sort_field)
      
    planets = db.session.scalars(query).all()
    planets_response = [planet.to_dict() for planet in planets]
    return planets_response

@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet_one(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "moon": planet.moon
    }

@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planets = Planet.query.all()
    planet = validate_planet(planet_id, planets)
    request_body = request.get_json()

    planet.name= request_body["name"]
    planet.description = request_body["description"]
    planet.moon= request_body["moon"]
    db.session.commit()

    return Response(status=204, mimetype="application/json") 

@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet_one(planet_id)
    db.session.delete(planet)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json") 

def validate_planet(planet_id, planets):
    # Narrow the errors - data error, type error
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"Planet id {planet_id} invalid"}, 400))

    for planet in planets:
        if planet.id == planet_id:
            return planet

    abort(make_response({"message": f"Planet {planet_id} not found"}, 404))


def validate_planet_one(planet_id):

    try:
        planet_id = int(planet_id)
    except:
        response = {"message": f"planet {planet_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)

    if not planet:
        response = {"message": f"{planet_id} not found"}
        abort(make_response(response, 404))

    return planet