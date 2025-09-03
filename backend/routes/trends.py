from flask import Blueprint, jsonify, request
from lib.db import DatabaseHelper

trends_bp = Blueprint('trends', __name__)
db = DatabaseHelper()

@trends_bp.route('/', methods=['GET'])
def get_trends():
    taxon_id = request.args.get('taxon_id')
    season = request.args.get('season')
    
    if not taxon_id and not season:
        return jsonify({'error': 'either taxon_id or season parameter is required'}), 400
    
    if taxon_id and season:
        return jsonify({'error': 'only one parameter allowed: taxon_id or season'}), 400
    
    if taxon_id:
        try:
            taxon_id_int = int(taxon_id)
        except ValueError:
            return jsonify({'error': 'taxon_id must be a valid integer'}), 400
        
        data = db.get_species_trend(taxon_id_int)

        if not data:
            return jsonify([])

        return jsonify(data)
    
    if season:
        valid_seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
        if season not in valid_seasons:
            return jsonify({'error': 'invalid season parameter'}), 400
        
        data = db.get_seasonal_trend(season)

        if not data:
            return jsonify([])

        return jsonify(data)
