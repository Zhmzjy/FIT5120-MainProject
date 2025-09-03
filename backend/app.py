import os
from flask import Flask, jsonify
from flask_cors import CORS
from routes.season import season_bp
from routes.top import top_bp
from routes.trends import trends_bp
from routes.species import species_bp
from routes.map import map_bp

app = Flask(__name__)
CORS(app)

@app.route('/')
def health_check():
    return jsonify({'status': 'ok', 'message': 'Wildlife Academy API is running'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

app.register_blueprint(season_bp, url_prefix='/api/season')
app.register_blueprint(top_bp, url_prefix='/api/season')
app.register_blueprint(trends_bp, url_prefix='/api/trends')
app.register_blueprint(species_bp, url_prefix='/api/species')
app.register_blueprint(map_bp, url_prefix='/api/map')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
