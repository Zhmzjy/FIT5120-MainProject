from flask import Blueprint, request, jsonify
from lib.db import get_db_connection
import logging

yearly_bp = Blueprint('yearly', __name__)

@yearly_bp.route('/most-common')
def get_yearly_most_common():
    try:
        year = request.args.get('year', type=int)
        if not year:
            return jsonify({'error': 'Year parameter is required'}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        SELECT 
            s.taxon_id,
            s.common_name,
            s.scientific_name,
            s.image_url,
            SUM(sc.count) as total_count
        FROM species s
        JOIN species_counts sc ON s.taxon_id = sc.taxon_id
        WHERE sc.year = %s
        GROUP BY s.taxon_id, s.common_name, s.scientific_name, s.image_url
        ORDER BY total_count DESC
        LIMIT 10
        """

        cursor.execute(query, (year,))
        results = cursor.fetchall()

        species_list = []
        for row in results:
            species_list.append({
                'taxonId': row[0],
                'commonName': row[1],
                'scientificName': row[2],
                'imageUrl': row[3] or '/images/koala.png',
                'count': row[4]
            })

        cursor.close()
        connection.close()

        return jsonify(species_list)

    except Exception as e:
        logging.error(f"Error getting yearly most common: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@yearly_bp.route('/least-common')
def get_yearly_least_common():
    try:
        year = request.args.get('year', type=int)
        if not year:
            return jsonify({'error': 'Year parameter is required'}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        SELECT 
            s.taxon_id,
            s.common_name,
            s.scientific_name,
            s.image_url,
            SUM(sc.count) as total_count
        FROM species s
        JOIN species_counts sc ON s.taxon_id = sc.taxon_id
        WHERE sc.year = %s AND sc.count > 0
        GROUP BY s.taxon_id, s.common_name, s.scientific_name, s.image_url
        ORDER BY total_count ASC
        LIMIT 10
        """

        cursor.execute(query, (year,))
        results = cursor.fetchall()

        species_list = []
        for row in results:
            species_list.append({
                'taxonId': row[0],
                'commonName': row[1],
                'scientificName': row[2],
                'imageUrl': row[3] or '/images/kangaroo.png',
                'count': row[4]
            })

        cursor.close()
        connection.close()

        return jsonify(species_list)

    except Exception as e:
        logging.error(f"Error getting yearly least common: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@yearly_bp.route('/compare')
def compare_years():
    try:
        year1 = request.args.get('year1', type=int)
        year2 = request.args.get('year2', type=int)

        if not year1 or not year2:
            return jsonify({'error': 'Both year1 and year2 parameters are required'}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        comparison_data = {
            'year1': {'mostCommon': [], 'leastCommon': [], 'totalSpecies': 0, 'totalObservations': 0},
            'year2': {'mostCommon': [], 'leastCommon': [], 'totalSpecies': 0, 'totalObservations': 0}
        }

        for year, year_key in [(year1, 'year1'), (year2, 'year2')]:
            most_common_query = """
            SELECT s.taxon_id, s.common_name, s.scientific_name, s.image_url, SUM(sc.count) as total_count
            FROM species s
            JOIN species_counts sc ON s.taxon_id = sc.taxon_id
            WHERE sc.year = %s
            GROUP BY s.taxon_id, s.common_name, s.scientific_name, s.image_url
            ORDER BY total_count DESC
            LIMIT 5
            """

            cursor.execute(most_common_query, (year,))
            most_common = cursor.fetchall()

            for row in most_common:
                comparison_data[year_key]['mostCommon'].append({
                    'taxonId': row[0],
                    'commonName': row[1],
                    'scientificName': row[2],
                    'imageUrl': row[3] or '/images/koala.png',
                    'count': row[4]
                })

            least_common_query = """
            SELECT s.taxon_id, s.common_name, s.scientific_name, s.image_url, SUM(sc.count) as total_count
            FROM species s
            JOIN species_counts sc ON s.taxon_id = sc.taxon_id
            WHERE sc.year = %s AND sc.count > 0
            GROUP BY s.taxon_id, s.common_name, s.scientific_name, s.image_url
            ORDER BY total_count ASC
            LIMIT 5
            """

            cursor.execute(least_common_query, (year,))
            least_common = cursor.fetchall()

            for row in least_common:
                comparison_data[year_key]['leastCommon'].append({
                    'taxonId': row[0],
                    'commonName': row[1],
                    'scientificName': row[2],
                    'imageUrl': row[3] or '/images/kangaroo.png',
                    'count': row[4]
                })

            stats_query = """
            SELECT 
                COUNT(DISTINCT s.taxon_id) as total_species,
                SUM(sc.count) as total_observations
            FROM species s
            JOIN species_counts sc ON s.taxon_id = sc.taxon_id
            WHERE sc.year = %s
            """

            cursor.execute(stats_query, (year,))
            stats = cursor.fetchone()

            comparison_data[year_key]['totalSpecies'] = stats[0] or 0
            comparison_data[year_key]['totalObservations'] = stats[1] or 0

        cursor.close()
        connection.close()

        return jsonify(comparison_data)

    except Exception as e:
        logging.error(f"Error comparing years: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@yearly_bp.route('/species-trend')
def get_species_yearly_trend():
    try:
        taxon_id = request.args.get('taxon_id', type=int)
        start_year = request.args.get('start_year', 2015, type=int)
        end_year = request.args.get('end_year', 2024, type=int)

        if not taxon_id:
            return jsonify({'error': 'taxon_id parameter is required'}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        SELECT sc.year, SUM(sc.count) as total_count
        FROM species_counts sc
        WHERE sc.taxon_id = %s AND sc.year BETWEEN %s AND %s
        GROUP BY sc.year
        ORDER BY sc.year
        """

        cursor.execute(query, (taxon_id, start_year, end_year))
        results = cursor.fetchall()

        trend_data = []
        for row in results:
            trend_data.append({
                'year': row[0],
                'count': row[1]
            })

        cursor.close()
        connection.close()

        return jsonify(trend_data)

    except Exception as e:
        logging.error(f"Error getting species yearly trend: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@yearly_bp.route('/available-years')
def get_available_years():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        SELECT DISTINCT year
        FROM species_counts
        ORDER BY year DESC
        """

        cursor.execute(query)
        results = cursor.fetchall()

        years = [row[0] for row in results]

        cursor.close()
        connection.close()

        return jsonify(years)

    except Exception as e:
        logging.error(f"Error getting available years: {e}")
        return jsonify({'error': 'Internal server error'}), 500
