from flask import Blueprint, jsonify, request
from lib.db import DatabaseHelper

map_bp = Blueprint('map', __name__)
db = DatabaseHelper()

@map_bp.route('/test', methods=['GET'])
def test_connection():
    try:
        query = "SELECT COUNT(*) as count FROM wildlife_observations"
        data = db.execute_query(query)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@map_bp.route('/stats', methods=['GET'])
def get_stats():
    try:
        total_observations_query = "SELECT COUNT(*) as total_observations FROM wildlife_observations"
        unique_species_query = "SELECT COUNT(DISTINCT scientific_name) as unique_species FROM wildlife_observations"

        total_obs = db.execute_query(total_observations_query)
        unique_species = db.execute_query(unique_species_query)

        return jsonify({
            'total_observations': total_obs[0]['total_observations'] if total_obs else 0,
            'unique_species': unique_species[0]['unique_species'] if unique_species else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@map_bp.route('/observations', methods=['GET'])
def get_observations():
    limit = request.args.get('limit', 500, type=int)
    limit = min(limit, 5000)
    state = request.args.get('state')
    region = request.args.get('region')
    conservation_status = request.args.get('conservation_status')
    animal_type = request.args.get('animal_type')
    search = request.args.get('search')
    
    where_conditions = ["wo.lat IS NOT NULL", "wo.lon IS NOT NULL"]
    params = {'limit': limit}
    
    if state:
        where_conditions.append("wo.state_territory = :state")
        params['state'] = state
    
    if region:
        where_conditions.append("wo.ibra_region = :region")
        params['region'] = region
    
    if conservation_status:
        where_conditions.append("wo.conservation_status = :conservation_status")
        params['conservation_status'] = conservation_status
    
    if animal_type:
        where_conditions.append("wo.kingdom = :animal_type")
        params['animal_type'] = animal_type
    
    if search:
        where_conditions.append("(wo.common_name ILIKE :search OR wo.scientific_name ILIKE :search)")
        params['search'] = f'%{search}%'
    
    where_clause = " AND ".join(where_conditions)
    
    query = f"""
    SELECT wo.scientific_name, wo.common_name, 
           wo.lat, wo.lon, 
           wo.state_territory, wo.ibra_region, wo.conservation_status,
           wo.occurrence_count, wo.kingdom as animal_type
    FROM wildlife_observations wo
    LEFT JOIN species s ON wo.scientific_name = s.scientific_name
    LEFT JOIN species_media sm ON s.taxon_id = sm.taxon_id
    WHERE {where_clause}
    ORDER BY wo.occurrence_count DESC
    LIMIT :limit
    """
    
    try:
        data = db.execute_query(query, params)
        if data is None:
            return jsonify({'error': 'Database connection failed'}), 500

        return jsonify({
            'observations': data,
            'total': len(data),
            'limit': limit
        })
    except Exception as e:
        return jsonify({'error': f'Query failed: {str(e)}'}), 500

@map_bp.route('/regions', methods=['GET'])
def get_regions():
    query = """
    SELECT 
        wo.ibra_region as name,
        wo.state_territory as state,
        COUNT(DISTINCT wo.scientific_name) as total_species,
        COUNT(*) as total_observations,
        COUNT(CASE WHEN wo.conservation_status IN ('Critically Endangered', 'Endangered', 'Vulnerable') THEN 1 END) as endangered_species,
        AVG(wo.lat) as center_lat,
        AVG(wo.lon) as center_lon
    FROM wildlife_observations wo
    WHERE wo.ibra_region IS NOT NULL AND wo.ibra_region != ''
    GROUP BY wo.ibra_region, wo.state_territory
    ORDER BY total_observations DESC
    """
    
    data = db.execute_query(query)
    
    if not data:
        return jsonify([])
    
    return jsonify(data)

@map_bp.route('/regions/<region_name>', methods=['GET'])
def get_region_details(region_name):
    stats_query = """
    SELECT 
        wo.ibra_region as name,
        wo.state_territory as state,
        COUNT(DISTINCT wo.scientific_name) as total_species,
        COUNT(*) as total_observations,
        COUNT(CASE WHEN wo.conservation_status IN ('Critically Endangered', 'Endangered', 'Vulnerable') THEN 1 END) as endangered_species
    FROM wildlife_observations wo
    WHERE wo.ibra_region = :region_name
    GROUP BY wo.ibra_region, wo.state_territory
    """
    
    top_species_query = """
    SELECT 
        wo.common_name,
        wo.scientific_name,
        COUNT(*) as count,
        st.iconic_taxon_name,
        sm.medium_url as image_url
    FROM wildlife_observations wo
    LEFT JOIN species_taxonomy st ON wo.scientific_name = st.scientific_name
    LEFT JOIN species_media sm ON st.taxon_id = sm.taxon_id
    WHERE wo.ibra_region = :region_name
    GROUP BY wo.common_name, wo.scientific_name, st.iconic_taxon_name, sm.medium_url
    ORDER BY count DESC
    LIMIT 10
    """
    
    stats = db.execute_query(stats_query, {"region_name": region_name})
    top_species = db.execute_query(top_species_query, {"region_name": region_name})
    
    if not stats:
        return jsonify({'error': 'Region not found'}), 404
    
    result = stats[0]
    result['top_species'] = top_species or []
    
    return jsonify(result)

@map_bp.route('/states', methods=['GET'])
def get_states():
    query = """
    SELECT 
        wo.state_territory as name,
        COUNT(DISTINCT wo.scientific_name) as total_species,
        COUNT(*) as total_observations,
        COUNT(CASE WHEN wo.conservation_status IN ('Critically Endangered', 'Endangered', 'Vulnerable') THEN 1 END) as endangered_species,
        COUNT(DISTINCT wo.ibra_region) as regions_count
    FROM wildlife_observations wo
    WHERE wo.state_territory IS NOT NULL AND wo.state_territory != ''
    GROUP BY wo.state_territory
    ORDER BY total_observations DESC
    """
    
    data = db.execute_query(query)
    
    if not data:
        return jsonify([])
    
    return jsonify(data)

@map_bp.route('/search', methods=['GET'])
def search_species():
    search = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)
    
    if not search:
        return jsonify([])
    
    query = """
    SELECT DISTINCT
        wo.common_name,
        wo.scientific_name,
        st.iconic_taxon_name,
        COUNT(*) as observation_count,
        sm.medium_url as image_url
    FROM wildlife_observations wo
    LEFT JOIN species_taxonomy st ON wo.scientific_name = st.scientific_name
    LEFT JOIN species_media sm ON st.taxon_id = sm.taxon_id
    WHERE LOWER(wo.common_name) LIKE LOWER(:search_term) 
       OR LOWER(wo.scientific_name) LIKE LOWER(:search_term)
    GROUP BY wo.common_name, wo.scientific_name, st.iconic_taxon_name, sm.medium_url
    ORDER BY observation_count DESC
    LIMIT :limit
    """
    
    search_term = f"%{search}%"
    data = db.execute_query(query, {"search_term": search_term, "limit": limit})
    
    if not data:
        return jsonify([])
    
    return jsonify(data)
