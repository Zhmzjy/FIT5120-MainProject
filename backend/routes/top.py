from flask import Blueprint, jsonify, request
from lib.db import DatabaseHelper

top_bp = Blueprint('top', __name__)
db = DatabaseHelper()

@top_bp.route('/top', methods=['GET'])
def get_top_species():
    season = request.args.get('season')
    if not season:
        return jsonify({'error': 'season parameter is required'}), 400
    
    valid_seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    if season not in valid_seasons:
        return jsonify({'error': 'invalid season parameter'}), 400
    
    data = db.get_top_species(season)

    if not data:
        return jsonify([])

    return jsonify(data)
