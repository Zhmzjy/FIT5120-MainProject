from flask import Blueprint, request, jsonify
from lib.db import DatabaseHelper
import logging

yearly_bp = Blueprint('yearly', __name__)
db = DatabaseHelper()

@yearly_bp.route('/most-common')
def get_yearly_most_common():
    try:
        year = request.args.get('year', type=int)
        if not year:
            return jsonify({'error': 'Year parameter is required'}), 400

        query = """
        SELECT 
            common_name,
            scientific_name,
            SUM(occurrence_count) as total_count
        FROM yearly_wildlife_occurrences
        WHERE year = :year
        GROUP BY common_name, scientific_name
        ORDER BY total_count DESC
        LIMIT 10
        """

        results = db.execute_query(query, {'year': year})

        species_list = []
        for row in results:
            species_list.append({
                'commonName': row['common_name'],
                'scientificName': row['scientific_name'],
                'count': row['total_count']
            })

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

        query = """
        SELECT 
            common_name,
            scientific_name,
            SUM(occurrence_count) as total_count
        FROM yearly_wildlife_occurrences
        WHERE year = :year AND occurrence_count > 0
        GROUP BY common_name, scientific_name
        ORDER BY total_count ASC
        LIMIT 10
        """

        results = db.execute_query(query, {'year': year})

        species_list = []
        for row in results:
            species_list.append({
                'commonName': row['common_name'],
                'scientificName': row['scientific_name'],
                'count': row['total_count']
            })

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

        comparison_data = {
            'year1': {'mostCommon': [], 'leastCommon': [], 'totalSpecies': 0, 'totalObservations': 0},
            'year2': {'mostCommon': [], 'leastCommon': [], 'totalSpecies': 0, 'totalObservations': 0}
        }

        for year, year_key in [(year1, 'year1'), (year2, 'year2')]:
            most_common_query = """
            SELECT common_name, scientific_name, SUM(occurrence_count) as total_count
            FROM yearly_wildlife_occurrences
            WHERE year = :year
            GROUP BY common_name, scientific_name
            ORDER BY total_count DESC
            LIMIT 5
            """

            most_common = db.execute_query(most_common_query, {'year': year})

            for row in most_common:
                comparison_data[year_key]['mostCommon'].append({
                    'commonName': row['common_name'],
                    'scientificName': row['scientific_name'],
                    'count': row['total_count']
                })

            least_common_query = """
            SELECT common_name, scientific_name, SUM(occurrence_count) as total_count
            FROM yearly_wildlife_occurrences
            WHERE year = :year AND occurrence_count > 0
            GROUP BY common_name, scientific_name
            ORDER BY total_count ASC
            LIMIT 5
            """

            least_common = db.execute_query(least_common_query, {'year': year})

            for row in least_common:
                comparison_data[year_key]['leastCommon'].append({
                    'commonName': row['common_name'],
                    'scientificName': row['scientific_name'],
                    'count': row['total_count']
                })

            stats_query = """
            SELECT 
                COUNT(DISTINCT common_name) as total_species,
                SUM(occurrence_count) as total_observations
            FROM yearly_wildlife_occurrences
            WHERE year = :year
            """

            stats = db.execute_query(stats_query, {'year': year})

            if stats and len(stats) > 0:
                comparison_data[year_key]['totalSpecies'] = stats[0]['total_species'] or 0
                comparison_data[year_key]['totalObservations'] = stats[0]['total_observations'] or 0

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

        query = """
        SELECT year, SUM(occurrence_count) as total_count
        FROM yearly_wildlife_occurrences
        WHERE common_name = :common_name AND year BETWEEN :start_year AND :end_year
        GROUP BY year
        ORDER BY year
        """

        results = db.execute_query(query, {
            'common_name': common_name,
            'start_year': start_year,
            'end_year': end_year
        })

        trend_data = []
        for row in results:
            trend_data.append({
                'year': row['year'],
                'count': row['total_count']
            })

        return jsonify(trend_data)

    except Exception as e:
        logging.error(f"Error getting species yearly trend: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@yearly_bp.route('/available-years')
def get_available_years():
    try:
        query = """
        SELECT DISTINCT year
        FROM yearly_wildlife_occurrences
        ORDER BY year DESC
        """

        results = db.execute_query(query)

        years = [row['year'] for row in results]

        return jsonify(years)

    except Exception as e:
        logging.error(f"Error getting available years: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@yearly_bp.route('/species-list')
def get_species_list():
    try:
        year = request.args.get('year', type=int)

        if year:
            query = """
            SELECT DISTINCT common_name, scientific_name
            FROM yearly_wildlife_occurrences
            WHERE year = :year
            ORDER BY common_name
            """
            results = db.execute_query(query, {'year': year})
        else:
            query = """
            SELECT DISTINCT common_name, scientific_name
            FROM yearly_wildlife_occurrences
            ORDER BY common_name
            """
            results = db.execute_query(query)

        species_list = []
        for row in results:
            species_list.append({
                'commonName': row['common_name'],
                'scientificName': row['scientific_name']
            })

        return jsonify(species_list)

    except Exception as e:
        logging.error(f"Error getting species list: {e}")
        return jsonify({'error': 'Internal server error'}), 500
