from flask import Blueprint, jsonify, request
from lib.db import DatabaseHelper
from lib.csv_fallback import CSVFallback

season_bp = Blueprint('season', __name__)
db = DatabaseHelper()
csv_fallback = CSVFallback()

@season_bp.route('/kpi', methods=['GET'])
def get_season_kpi():
    data = db.get_season_kpi()
    if not data:
        data = csv_fallback.get_season_kpi()
    
    if not data:
        return jsonify([]), 404
    
    return jsonify(data)

@season_bp.route('/activity', methods=['GET'])
def get_season_activity():
    data = db.get_season_activity()
    if not data:
        data = csv_fallback.get_season_activity()
    
    if not data:
        return jsonify([]), 404
    
    return jsonify(data)
