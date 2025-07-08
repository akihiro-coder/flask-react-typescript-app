from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
import redis

# 環境変数を読み込み
load_dotenv()

# Flask アプリケーションの初期化
app = Flask(__name__)

# 設定
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/voting_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 拡張機能の初期化
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(','))
socketio = SocketIO(app, cors_allowed_origins=os.getenv('SOCKETIO_CORS_ALLOWED_ORIGINS', 'http://localhost:5173'))

# Redis接続
redis_client = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'))

# ルートエンドポイント
@app.route('/')
def index():
    return {'message': 'Real-time Voting App API', 'status': 'running'}

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
