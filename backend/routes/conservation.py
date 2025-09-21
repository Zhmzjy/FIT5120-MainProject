from flask import Blueprint, jsonify, request
from lib.db import DatabaseHelper

conservation_bp = Blueprint('conservation', __name__)

@conservation_bp.route('/species', methods=['GET'])
def get_conservation_species():
    try:
        db = DatabaseHelper()

        target_species = [
            'Tasmanian Devil',
            'Southern Cassowary',
            'Sharp-tailed Sandpiper',
            'Grey-headed Flying-fox',
            'Gang-gang Cockatoo',
            'Koala'
        ]

        query = """
        SELECT DISTINCT 
            s.common_name, 
            s.scientific_name, 
            s.image_url,
            w.conservation_status
        FROM species s 
        JOIN wildlife_observations w ON s.common_name = w.common_name 
        WHERE s.common_name = ANY(%s)
        AND w.conservation_status IS NOT NULL
        """

        results = db.execute_query(query, [target_species])

        if not results:
            return jsonify([])

        species_data = []
        for row in results:
            common_name = row['common_name']
            scientific_name = row['scientific_name']
            image_url = row['image_url']
            conservation_status = row['conservation_status']

            status_class = ''
            if conservation_status == 'Critically Endangered':
                status_class = 'critically-endangered'
            elif conservation_status == 'Endangered':
                status_class = 'endangered'
            elif conservation_status == 'Vulnerable':
                status_class = 'vulnerable'

            description = get_species_description(common_name)
            threat = get_species_threat(common_name)

            species_data.append({
                'id': len(species_data) + 1,
                'name': common_name,
                'scientific_name': scientific_name,
                'image': image_url,
                'status': conservation_status,
                'statusClass': status_class,
                'description': description,
                'threat': threat
            })

        return jsonify(species_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_species_description(common_name):
    descriptions = {
        'Tasmanian Devil': 'These fierce little animals live only in Tasmania and are known for their loud screeches.',
        'Southern Cassowary': 'Large flightless birds with distinctive casques on their heads, found in rainforests.',
        'Sharp-tailed Sandpiper': 'Migratory shorebirds that travel thousands of kilometers between breeding and feeding grounds.',
        'Grey-headed Flying-fox': 'Large fruit bats that play crucial roles in pollinating native plants and dispersing seeds.',
        'Gang-gang Cockatoo': 'Distinctive grey cockatoos with bright red heads, found in mountain forests and woodlands.',
        'Koala': 'These sleepy marsupials spend most of their time in eucalyptus trees.'
    }
    return descriptions.get(common_name, 'An important Australian native species.')

def get_species_threat(common_name):
    threats = {
        'Tasmanian Devil': 'Disease and habitat loss',
        'Southern Cassowary': 'Habitat destruction and vehicle strikes',
        'Sharp-tailed Sandpiper': 'Coastal development and climate change',
        'Grey-headed Flying-fox': 'Habitat loss and extreme heat events',
        'Gang-gang Cockatoo': 'Bushfires and habitat fragmentation',
        'Koala': 'Deforestation and bushfires'
    }
    return threats.get(common_name, 'Habitat loss and human activities')

@conservation_bp.route('/daily-animal', methods=['GET'])
def get_daily_animal():
    try:
        db = DatabaseHelper()

        query = """
        SELECT DISTINCT 
            s.common_name, 
            s.scientific_name, 
            s.image_url
        FROM species s 
        JOIN wildlife_observations w ON s.common_name = w.common_name 
        WHERE s.common_name = 'Koala'
        AND s.image_url IS NOT NULL
        LIMIT 1
        """

        results = db.execute_query(query)

        if not results:
            return jsonify({
                'common_name': 'Koala',
                'scientific_name': 'Phascolarctos cinereus',
                'image_url': '/images/koala.png'
            })

        row = results[0]
        return jsonify({
            'common_name': row['common_name'],
            'scientific_name': row['scientific_name'],
            'image_url': row['image_url']
        })

    except Exception as e:
        return jsonify({
            'common_name': 'Koala',
            'scientific_name': 'Phascolarctos cinereus',
            'image_url': '/images/koala.png'
        }), 200
