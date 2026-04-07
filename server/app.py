# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    if earthquake:
        body = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }
        status = 200
    else:
        body = {
            'message': f'Earthquake {id} not found.'
        }
        status = 404
    return make_response(body, status)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_by_magnitude(magnitude):
    quakes = []
    #this filters earthquakes with magnitude greater than or equal to the specified magnitude and less than the next whole number
    #we don't expect total equality because of the nature of earthquake magnitudes, but this allows us to group earthquakes by their whole number magnitude
    #we look at a certain range since we are dealing with floats, and we want to include earthquakes that are close to the specified magnitude but may not be exactly equal due to decimal precision
    for e in Earthquake.query.filter(
        Earthquake.magnitude >= magnitude,
        Earthquake.magnitude < magnitude + 1
    ).all():
            e_dict = {
                'id': e.id,
                'magnitude': e.magnitude,
                "location": e.location,
                'year': e.year
            }
            quakes.append(e_dict)
    body = {'count': len(quakes),
            'quakes': quakes}
            
    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
