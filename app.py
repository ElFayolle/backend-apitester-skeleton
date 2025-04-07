import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'


# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

@app.route('/api/alive', methods=['GET'])
def alive():
    return jsonify({"message": "Alive"}), 200

@app.route('/api/associations', methods=['GET'])
def get_associations():
    return jsonify(associations_df['nom'].tolist()), 200

@app.route('/api/association/<int:id>', methods=['GET'])
def get_association(id):
    assoc = associations_df[associations_df['id'] == id]
    if assoc.empty:
        return jsonify({"error": "Association not found"}), 404
    return jsonify(assoc.iloc[0].to_dict()), 200


@app.route('/api/evenements', methods=['GET'])
def get_evenements():
   return jsonify(evenements_df['id'].tolist()), 200


@app.route('/api/evenement/<int:id>', methods=['GET'])
def get_evenement(id):
    event = evenements_df[evenements_df['id'] == id]
    if event.empty:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.iloc[0].to_dict()), 200

@app.route('/api/association/<int:id>/evenements', methods=['GET'])
def get_evenements_by_association(id):
    events = evenements_df[evenements_df['association_id'] == id]
    return jsonify(events.to_dict(orient='records')), 200

@app.route('/api/associations/type/<asso>', methods=['GET'])
def get_associations_by_type(asso):
    filtered = associations_df[associations_df['type'].str.lower() == type.lower()]
    return jsonify(filtered.to_dict(orient='records')), 200



if __name__ == '__main__':
    app.run(debug=False)
