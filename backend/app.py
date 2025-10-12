import os
from flask import Flask, jsonify
from flask_cors import CORS
from routes.season import season_bp
from routes.top import top_bp
from routes.trends import trends_bp
from routes.species import species_bp
from routes.map import map_bp
from routes.conservation import conservation_bp
from routes.ai_challenge import ai_challenge_bp, init_ai_challenge
from routes.daily_wildle import daily_wildle_bp, init_daily_wildle
from routes.audio import audio_bp

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.route('/')
def health_check():
    return jsonify({'status': 'ok', 'message': 'Wildlife Academy API is running'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

app.register_blueprint(season_bp, url_prefix='/api/season')
app.register_blueprint(top_bp, url_prefix='/api/top')
app.register_blueprint(trends_bp, url_prefix='/api/trends')
app.register_blueprint(species_bp, url_prefix='/api/species')
app.register_blueprint(map_bp, url_prefix='/api/map')
app.register_blueprint(conservation_bp, url_prefix='/api/conservation')
app.register_blueprint(ai_challenge_bp, url_prefix='/api/ai-challenge')
app.register_blueprint(daily_wildle_bp, url_prefix='/api/daily-wildle')
app.register_blueprint(audio_bp, url_prefix='/api/audio')

try:
    init_ai_challenge()
    print("AI Challenge initialized successfully")
except Exception as e:
    print(f"Warning: AI Challenge initialization failed: {e}")

try:
    init_daily_wildle()
    print("Daily Wildle initialized successfully")
except Exception as e:
    print(f"Warning: Daily Wildle initialization failed: {e}")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
