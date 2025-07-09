# リアルタイム投票アプリ

Python Flask + TypeScript React + PostgreSQL + Heroku を使用したシンプルなリアルタイム投票アプリケーション。Flask、React、TypeScriptの学習を目的とした一日ハッカソンプロジェクトです。

## 🎯 MVP機能

- 投票ルーム作成（質問 + 選択肢）
- 投票ルーム参加（ルームコード入力）
- リアルタイム投票
- リアルタイム結果表示（棒グラフ）
- 投票終了機能

## 🔧 技術スタック

- **バックエンド**: Flask + Flask-SocketIO + SQLAlchemy + Redis
- **フロントエンド**: React + TypeScript + Redux + Socket.IO + Tailwind CSS
- **データベース**: PostgreSQL
- **リアルタイム**: WebSocket (Socket.IO)

## 🗄️ データベース設計

### ER図

```
┌─────────────────────────────────┐
│          VotingRoom             │
├─────────────────────────────────┤
│ PK id (Integer)                 │
│    room_code (String, 6)        │
│    title (String, 200)          │
│    description (Text)           │
│    is_active (Boolean)          │
│    created_at (DateTime)        │
│    ended_at (DateTime)          │
└─────────────────────────────────┘
                │
                │ 1:N
                ▼
┌─────────────────────────────────┐
│         VotingOption            │
├─────────────────────────────────┤
│ PK id (Integer)                 │
│ FK room_id (Integer)            │
│    text (String, 200)           │
│    order (Integer)              │
└─────────────────────────────────┘
                │
                │ 1:N
                ▼
┌─────────────────────────────────┐
│            Vote                 │
├─────────────────────────────────┤
│ PK id (Integer)                 │
│ FK room_id (Integer)            │
│ FK option_id (Integer)          │
│    voter_session (String, 100)  │
│    voted_at (DateTime)          │
└─────────────────────────────────┘

UNIQUE(room_id, voter_session)
```

### モデル関係性

#### 1. VotingRoom ↔ VotingOption (1:N)
- 1つの投票ルームには複数の選択肢が存在
- 選択肢は必ず1つのルームに属する

#### 2. VotingRoom ↔ Vote (1:N)
- 1つの投票ルームには複数の投票が存在
- 投票は必ず1つのルームに属する

#### 3. VotingOption ↔ Vote (1:N)
- 1つの選択肢には複数の投票が可能
- 投票は必ず1つの選択肢に対して行われる

### ユニーク制約

```sql
UNIQUE(room_id, voter_session)
```

**目的**: 同じセッション（ユーザー）は同じルームで1回のみ投票可能

#### 具体例

**投票ルーム**: ROOM123「好きな色は？」
- 選択肢: 赤、青、緑

**正常なケース**:
| ユーザー | セッションID | 投票 | 結果 |
|----------|--------------|------|------|
| 太郎 | session_abc123 | 赤 | ✅ 成功 |
| 花子 | session_def456 | 青 | ✅ 成功 |
| 太郎 | session_abc123 | 別ルームで投票 | ✅ 成功（異なるルーム） |

**エラーケース**:
| ユーザー | セッションID | 投票 | 結果 |
|----------|--------------|------|------|
| 太郎 | session_abc123 | 緑（2回目） | ❌ エラー：既に投票済み |

### セッション管理

#### voter_sessionとは
- ユーザーを識別するための一意のID
- ユーザー登録不要で重複投票を防止
- ブラウザのsessionStorageに保存

#### 実装例

```typescript
// セッションID生成
const getVoterSession = () => {
  let session = sessionStorage.getItem('voter_session');
  if (!session) {
    session = Date.now().toString() + Math.random().toString(36).substr(2);
    sessionStorage.setItem('voter_session', session);
  }
  return session;
};

// 投票時
const vote = async (optionId: number) => {
  const sessionId = getVoterSession();

  await api.post('/vote', {
    room_id: roomId,
    option_id: optionId,
    voter_session: sessionId
  });
};
```

#### セッションの種類

| 種類 | 保存場所 | 特徴 |
|------|----------|------|
| sessionStorage | ブラウザタブ | タブを閉じると消える |
| localStorage | ブラウザ | ブラウザを閉じても残る |
| Cookie | ブラウザ | 有効期限設定可能 |

### データフロー例

#### 1. ルーム作成フロー
```
ユーザー → フロントエンド → API `/rooms` → VotingRoom作成
                                        → VotingOption作成（複数）
                                        → room_code返却
```

#### 2. 投票フロー
```
ユーザー → フロントエンド → API `/vote` → 重複チェック（voter_session）
                                       → Vote作成
                                       → WebSocket → 全クライアントに結果配信
```

#### 3. 結果表示フロー
```
WebSocket受信 → Redux store更新 → React re-render → チャート更新
```

## 🚀 セットアップ

### バックエンド

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# データベースマイグレーション
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# サーバー起動
python app.py
```

### フロントエンド

```bash
cd frontend
npm install
npm run dev
```

### 環境変数

```bash
# backend/.env
DATABASE_URL=postgresql://postgres:password@localhost:5432/voting_app
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:5173
```

## 📁 プロジェクト構造

```
flask-react-typescript-app/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── room.py
│   │   │   ├── option.py
│   │   │   └── vote.py
│   │   ├── routes/
│   │   └── sockets/
│   ├── app.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   └── types/
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 📝 開発進捗

- ✅ Phase 1: プロジェクト基盤構築
- ✅ Phase 2: データベース設計
- ⏳ Phase 3: バックエンドAPI開発
- ⏳ Phase 4: フロントエンド開発
- ⏳ Phase 5: 統合・テスト
- ⏳ Phase 6: デプロイ準備

## 🎯 学習目標

- Flask でのRESTful API設計
- Flask-SocketIO でのリアルタイム通信
- React + TypeScript でのコンポーネント設計
- Redux での状態管理
- PostgreSQL でのリレーショナルデータベース設計
- WebSocketを使ったリアルタイムアプリケーション開発
