from flask import Flask
from flask_cors import CORS
from routes.season import season_bp
from routes.top import top_bp
from routes.trends import trends_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(season_bp, url_prefix='/api/season')
app.register_blueprint(top_bp, url_prefix='/api/season')
app.register_blueprint(trends_bp, url_prefix='/api/trends')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
