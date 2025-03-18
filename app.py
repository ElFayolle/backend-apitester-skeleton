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

## Vous devez ajouter les routes ici : 

@app.route('/api/alive')
def alive():
    # no need to explicitly jsonify a dict,
    # Flask will do it for you
    return {'message': 'Alive'}

def json_compat(int64):
    if isinstance(int64, np.int64):
        return int(int64)
    return int64

@app.route('/api/associations')
def list_associations():
    df = pd.read_csv("data/associations_etudiantes.csv")
    # we need to explicitly convert to int because
    # numpy's int64 is not serializable to JSON
    # otoh it would in theory be possible to return an iterable
    # in which case flask would produce an HTTP stream
    # but that would require the frontend to handle it properly
    # so we build a list of ints and explicitly jsonify it
    return jsonify(
        [json_compat(assoc_id) for assoc_id in df['id'].values]
    )

@app.route('/api/association/<int:assoc_id>')
def association_details(assoc_id):
    df = pd.read_csv(data / "associations_etudiantes.csv")
    row_df = df[df.id == assoc_id]
    if len(row_df) == 0:
        print(f" id {assoc_id} not found")
        return ({'error': f'unknown id {assoc_id}'}, 404)
    return jsonify(
        [json_compat(x) for x in row_df.iloc[0]]
    )

@app.route("/api/evenements")
def list_evenements():
    df = pd.read_csv(data / "evenements_associations.csv")
    return jsonify(
        [json_compat(event_id) for event_id in df['id'].values]
    )

@app.route("/api/evenement/<int:event_id>")
def evenement_details(event_id):
    df = pd.read_csv(data / "evenements_associations.csv")
    row_df = df[df.id == event_id]
    if len(row_df) == 0:
        print(f" id {event_id} not found")
        return ({'error': f'unknown id {event_id}'}, 404)
    return jsonify(
        [json_compat(x) for x in row_df.iloc[0]]
    )

@app.route("/api/association/<int:assoc_id>/evenements")
def evenements_association(assoc_id):
    events = pd.read_csv(data / "evenements_associations.csv")
    assocs = pd.read_csv(data / "associations_etudiantes.csv")
    df = (
        pd.merge(assocs, events, left_on='id', right_on='association_id')
        .drop(columns=['association_id'])
        .rename(columns={'id_x': 'id'})
    )
    assoc_events = df[df.id == assoc_id]
    return jsonify(
        assoc_events.to_dict(orient='records')
    )


if __name__ == '__main__':
    app.run(debug=False)
