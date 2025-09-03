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
