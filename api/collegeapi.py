from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # To handle cross-origin requests
import pandas as pd
import csv
import json

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///colleges.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50))
    weather = db.Column(db.String(50))
    public_private = db.Column(db.String(50))
    population_size = db.Column(db.String(50))
    tuition_preference = db.Column(db.String(50))
    orientation = db.Column(db.String(100))

def initialize_database():
    db.create_all()  # Creates the database tables
    if not College.query.first():  # Checks if the database is empty
        load_data()  # Load data if database is empty

def load_data():
    data = pd.read_csv('/path/to/Final_Extended_Real_College_Dataset.csv')
    for _, row in data.iterrows():
        college = College(
            name=row['College Name'],
            location=row['Location'],
            weather=row['Weather'],
            public_private=row['Public/Private'],
            population_size=row['Population Size'],
            tuition_preference=row['Tuition Preference'],
            orientation=row['Orientation']
        )
        db.session.add(college)
    db.session.commit()

college_api = Blueprint('college_api', __name__, url_prefix='/api/college')


@college_api.route('/colleges', methods=['POST'])
def get_colleges():
    
    data = {}
     

    with open(r'College_Dataset.csv', encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        for rows in csvReader:
            key = rows['College Name']
            data[key] = rows

    return((data))

if __name__ == '__main__':
    initialize_database()  # Initialize database when starting the app
    app.run(debug=True)
