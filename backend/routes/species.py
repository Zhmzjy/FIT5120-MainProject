from flask import Blueprint, jsonify, request
from lib.db import DatabaseHelper
from lib.csv_fallback import CSVFallback

species_bp = Blueprint('species', __name__)
db = DatabaseHelper()
csv_fallback = CSVFallback()

@species_bp.route('/', methods=['GET'])
def get_species_list():
    search = request.args.get('search', '')
    limit = request.args.get('limit', 50, type=int)
    
    query = """
    SELECT taxon_id, common_name, scientific_name, image_url 
    FROM species 
    WHERE LOWER(common_name) LIKE LOWER(%s) 
       OR LOWER(scientific_name) LIKE LOWER(%s)
    ORDER BY common_name
    LIMIT %s
    """
    
    search_term = f"%{search}%"
    data = db.execute_query(query, [search_term, search_term, limit])
    
    if not data:
        return jsonify([])
    
    return jsonify(data)

@species_bp.route('/<int:taxon_id>', methods=['GET'])
def get_species_detail(taxon_id):
    query = """
    SELECT s.taxon_id, s.common_name, s.scientific_name, s.image_url,
           COUNT(sc.id) as observation_count,
           SUM(sc.count) as total_count
    FROM species s
    LEFT JOIN species_counts sc ON s.taxon_id = sc.taxon_id
    WHERE s.taxon_id = %s
    GROUP BY s.taxon_id, s.common_name, s.scientific_name, s.image_url
    """
    
    data = db.execute_query(query, [taxon_id])
    
    if not data:
        return jsonify({'error': 'Species not found'}), 404
    
    return jsonify(data[0])
