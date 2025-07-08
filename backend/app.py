from dotenv import load_dotenv
import os

# 環境変数を読み込み（最初に実行）
load_dotenv()

from app import create_app, db, socketio

# アプリケーションを作成
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 開発環境でテーブルを自動作成
        try:
            db.create_all()
            print("✅ Database tables created")
        except Exception as e:
            print(f"❌ Database error: {e}")

    print("🚀 Starting Real-time Voting App...")
    print("📊 Database:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("🔄 Redis:", os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
    print("🌐 CORS origins:", os.getenv('CORS_ORIGINS', 'http://localhost:5173'))

    # SocketIOでアプリケーションを起動
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
