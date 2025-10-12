from flask import Blueprint, jsonify, send_file, request
from lib.db import DatabaseHelper
import os

audio_bp = Blueprint('audio', __name__)
db = DatabaseHelper()

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'species_sound_file')

@audio_bp.route('/sounds', methods=['GET'])
def get_all_sounds():
    query = """
        SELECT id, common_name, scientific_name, sound_url
        FROM animal_sounds
        ORDER BY common_name
    """

    result = db.execute_query(query)

    if not result:
        return jsonify([])

    sounds = []
    for row in result:
        sounds.append({
            'id': row['id'],
            'commonName': row['common_name'],
            'scientificName': row['scientific_name'],
            'soundUrl': row['sound_url']
        })

    return jsonify(sounds)

@audio_bp.route('/random', methods=['GET'])
def get_random_sounds():
    count = request.args.get('count', 5, type=int)

    query = """
        SELECT id, common_name, scientific_name, sound_url
        FROM animal_sounds
        ORDER BY RANDOM()
        LIMIT :count
    """

    result = db.execute_query(query, {'count': count})

    if not result:
        return jsonify([])

    sounds = []
    for row in result:
        sounds.append({
            'id': row['id'],
            'commonName': row['common_name'],
            'scientificName': row['scientific_name'],
            'soundUrl': row['sound_url']
        })

    return jsonify(sounds)

@audio_bp.route('/details/<int:animal_id>', methods=['GET'])
def get_animal_details(animal_id):
    query = """
        SELECT ad.common_name, ad.scientific_name, ad.description, 
               ad.habitat, ad.diet, ad.conservation_status, ad.fun_fact,
               asound.sound_url
        FROM animal_details ad
        LEFT JOIN animal_sounds asound ON ad.common_name = asound.common_name
        WHERE ad.id = :animal_id
    """

    result = db.execute_query(query, {'animal_id': animal_id})

    if not result or len(result) == 0:
        return jsonify({'error': 'Animal not found'}), 404

    row = result[0]
    details = {
        'commonName': row['common_name'],
        'scientificName': row['scientific_name'],
        'description': row['description'],
        'habitat': row['habitat'],
        'diet': row['diet'],
        'conservationStatus': row['conservation_status'],
        'funFact': row['fun_fact'],
        'soundUrl': row['sound_url']
    }

    return jsonify(details)

@audio_bp.route('/<filename>', methods=['GET'])
def serve_audio_file(filename):
    try:
        file_path = os.path.join(AUDIO_DIR, filename)

        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        return send_file(file_path, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
