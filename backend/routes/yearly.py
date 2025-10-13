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
            common_name,
            scientific_name,
            SUM(occurrence_count) as total_count
        FROM yearly_wildlife_occurrences
        WHERE year = %s
        GROUP BY common_name, scientific_name
        ORDER BY total_count DESC
        LIMIT 10
        """

        cursor.execute(query, (year,))
        results = cursor.fetchall()

        species_list = []
        for row in results:
            species_list.append({
                'commonName': row[0],
                'scientificName': row[1],
                'count': row[2]
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
            common_name,
            scientific_name,
            SUM(occurrence_count) as total_count
        FROM yearly_wildlife_occurrences
        WHERE year = %s AND occurrence_count > 0
        GROUP BY common_name, scientific_name
        ORDER BY total_count ASC
        LIMIT 10
        """

        cursor.execute(query, (year,))
        results = cursor.fetchall()

        species_list = []
        for row in results:
            species_list.append({
                'commonName': row[0],
                'scientificName': row[1],
                'count': row[2]
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
            SELECT common_name, scientific_name, SUM(occurrence_count) as total_count
            FROM yearly_wildlife_occurrences
            WHERE year = %s
            GROUP BY common_name, scientific_name
            ORDER BY total_count DESC
            LIMIT 5
            """

            cursor.execute(most_common_query, (year,))
            most_common = cursor.fetchall()

            for row in most_common:
                comparison_data[year_key]['mostCommon'].append({
                    'commonName': row[0],
                    'scientificName': row[1],
                    'count': row[2]
                })

            least_common_query = """
            SELECT common_name, scientific_name, SUM(occurrence_count) as total_count
            FROM yearly_wildlife_occurrences
            WHERE year = %s AND occurrence_count > 0
            GROUP BY common_name, scientific_name
            ORDER BY total_count ASC
            LIMIT 5
            """

            cursor.execute(least_common_query, (year,))
            least_common = cursor.fetchall()

            for row in least_common:
                comparison_data[year_key]['leastCommon'].append({
                    'commonName': row[0],
                    'scientificName': row[1],
                    'count': row[2]
                })

            stats_query = """
            SELECT 
                COUNT(DISTINCT common_name) as total_species,
                SUM(occurrence_count) as total_observations
            FROM yearly_wildlife_occurrences
            WHERE year = %s
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
        common_name = request.args.get('common_name')
        start_year = request.args.get('start_year', 1970, type=int)
        end_year = request.args.get('end_year', 2022, type=int)

        if not common_name:
            return jsonify({'error': 'common_name parameter is required'}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        SELECT year, SUM(occurrence_count) as total_count
        FROM yearly_wildlife_occurrences
        WHERE common_name = %s AND year BETWEEN %s AND %s
        GROUP BY year
        ORDER BY year
        """

        cursor.execute(query, (common_name, start_year, end_year))
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
        FROM yearly_wildlife_occurrences
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

@yearly_bp.route('/species-list')
def get_species_list():
    try:
        year = request.args.get('year', type=int)

        connection = get_db_connection()
        cursor = connection.cursor()

        if year:
            query = """
            SELECT DISTINCT common_name, scientific_name
            FROM yearly_wildlife_occurrences
            WHERE year = %s
            ORDER BY common_name
            """
            cursor.execute(query, (year,))
        else:
            query = """
            SELECT DISTINCT common_name, scientific_name
            FROM yearly_wildlife_occurrences
            ORDER BY common_name
            """
            cursor.execute(query)

        results = cursor.fetchall()

        species_list = []
        for row in results:
            species_list.append({
                'commonName': row[0],
                'scientificName': row[1]
            })

        cursor.close()
        connection.close()

        return jsonify(species_list)

    except Exception as e:
        logging.error(f"Error getting species list: {e}")
        return jsonify({'error': 'Internal server error'}), 500
