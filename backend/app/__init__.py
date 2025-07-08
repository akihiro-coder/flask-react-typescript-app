from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_socketio import SocketIO
import redis
import os

# 拡張機能をグローバルに初期化（アプリケーションは後で設定）
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
socketio = SocketIO()
redis_client = None

def create_app():
    """アプリケーションファクトリ"""
    app = Flask(__name__)

    # 設定
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///voting_app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 拡張機能をアプリに登録
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(','))
    socketio.init_app(app, cors_allowed_origins=os.getenv('SOCKETIO_CORS_ALLOWED_ORIGINS', 'http://localhost:5173'))

    # Redis接続（オプション）
    global redis_client
    try:
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        redis_client = redis.from_url(redis_url)
        redis_client.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"⚠️  Redis not available (continuing without Redis): {e}")
        redis_client = None

    # モデルをインポート（dbが初期化された後）
    from app.models import VotingRoom, VotingOption, Vote

    # ルート登録
    register_routes(app)

    return app

def register_routes(app):
    """ルートを登録"""
    @app.route('/')
    def index():
        return {
            'message': 'Real-time Voting App API',
            'status': 'running',
            'version': '1.0.0',
            'database': 'connected' if db else 'disconnected'
        }

    @app.route('/health')
    def health():
        db_status = 'connected'
        redis_status = 'connected' if redis_client else 'not available'

        try:
            # データベース接続テスト
            db.session.execute(db.text('SELECT 1'))
        except Exception as e:
            db_status = f'error: {str(e)}'

        return {
            'status': 'healthy',
            'database': db_status,
            'redis': redis_status
        }
