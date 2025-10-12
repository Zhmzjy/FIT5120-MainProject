from flask import Blueprint, jsonify, send_file
import os

audio_bp = Blueprint('audio', __name__)

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'species_sound_file')

@audio_bp.route('/sounds', methods=['GET'])
def get_all_sounds():
    from lib.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, common_name, scientific_name, sound_url
        FROM animal_sounds
        ORDER BY common_name
    """)

    sounds = []
    for row in cursor.fetchall():
        sounds.append({
            'id': row[0],
            'commonName': row[1],
            'scientificName': row[2],
            'soundUrl': row[3]
        })

    cursor.close()
    conn.close()

    return jsonify(sounds)

@audio_bp.route('/random', methods=['GET'])
def get_random_sounds():
    from flask import request
    from lib.db import get_db_connection

    count = request.args.get('count', 5, type=int)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, common_name, scientific_name, sound_url
        FROM animal_sounds
        ORDER BY RANDOM()
        LIMIT %s
    """, (count,))

    sounds = []
    for row in cursor.fetchall():
        sounds.append({
            'id': row[0],
            'commonName': row[1],
            'scientificName': row[2],
            'soundUrl': row[3]
        })

    cursor.close()
    conn.close()

    return jsonify(sounds)

@audio_bp.route('/details/<name>', methods=['GET'])
def get_animal_details(name):
    from lib.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT common_name, scientific_name, year, conservation_status,
               occurrence_count, taxon_class, body_mass_g, size_category,
               diet_type, foraging_behavior, activity_pattern, is_nocturnal,
               can_fly, can_swim, eats_insects, eats_fruit, eats_fish,
               is_marsupial, is_bat, habitats
        FROM animal_details
        WHERE common_name = %s
    """, (name,))

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return jsonify({'error': 'Animal not found'}), 404

    return jsonify({
        'commonName': row[0],
        'scientificName': row[1],
        'year': row[2],
        'conservationStatus': row[3],
        'occurrenceCount': row[4],
        'taxonClass': row[5],
        'bodyMass': float(row[6]) if row[6] else None,
        'sizeCategory': row[7],
        'dietType': row[8],
        'foragingBehavior': row[9],
        'activityPattern': row[10],
        'isNocturnal': row[11],
        'canFly': row[12],
        'canSwim': row[13],
        'eatsInsects': row[14],
        'eatsFruit': row[15],
        'eatsFish': row[16],
        'isMarsupial': row[17],
        'isBat': row[18],
        'habitats': row[19]
    })

@audio_bp.route('/<filename>', methods=['GET'])
def serve_audio_file(filename):
    try:
        file_path = os.path.join(AUDIO_DIR, filename)

        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        return send_file(file_path, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

