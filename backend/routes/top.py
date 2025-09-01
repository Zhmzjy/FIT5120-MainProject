from flask import Blueprint, jsonify, request
from lib.db import DatabaseHelper
from lib.csv_fallback import CSVFallback

top_bp = Blueprint('top', __name__)
db = DatabaseHelper()
csv_fallback = CSVFallback()

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
        data = csv_fallback.get_top_species(season)
    
    if not data:
        return jsonify([]), 404
    
    return jsonify(data)
