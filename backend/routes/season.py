from flask import Blueprint, jsonify, request
from lib.db import DatabaseHelper

season_bp = Blueprint('season', __name__)
db = DatabaseHelper()

@season_bp.route('/kpi', methods=['GET'])
def get_season_kpi():
    data = db.get_season_kpi()

    if not data:
        return jsonify([])

    return jsonify(data)

@season_bp.route('/activity', methods=['GET'])
def get_season_activity():
    data = db.get_season_activity()

    if not data:
        return jsonify([])

    return jsonify(data)

@season_bp.route('/monthly-trends', methods=['GET'])
def get_monthly_trends():
    season = request.args.get('season')

    if not season:
        return jsonify({'error': 'season parameter is required'}), 400

    valid_seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    if season not in valid_seasons:
        return jsonify({'error': 'invalid season parameter'}), 400

    data = db.get_season_monthly_trends(season)

    if not data:
        return jsonify([])

    return jsonify(data)
