# プロジェクトの目的
- このプロジェクトは、Python, Flask, TypeScript, React, PostgreSQL, Herokuを使用して、とてもシンプルなアプリケーションを作成することを目的としています。
- Flask, React, TypeScriptで何ができるか学ぶためのプロジェクトです。　
- リアルタイム投票アプリを一日で開発するための作業計画は以下のとおりです。

# 📋 一日ハッカソン開発計画

## 🏗️ **Phase 1: プロジェクト基盤構築** (1-2時間)
- [ ] プロジェクトディレクトリ構造の作成
- [ ] バックエンド環境設定（Flask、requirements.txt）
- [ ] フロントエンド環境設定（React + TypeScript、package.json）
- [ ] 環境変数設定（.env）
- [ ] PostgreSQL + Redis 接続設定
- [ ] CORS設定

## 🗄️ **Phase 2: データベース設計** (30分)
- [ ] 投票ルームモデル設計
- [ ] 投票選択肢モデル設計
- [ ] 投票記録モデル設計
- [ ] データベースマイグレーション設定

## 🔧 **Phase 3: バックエンドAPI開発** (2-3時間)
- [ ] Flask-SocketIOセットアップ
- [ ] 投票ルーム作成・取得API
- [ ] 投票機能API
- [ ] リアルタイム結果配信（WebSocket）
- [ ] Redis活用（セッション・キャッシュ）

## 🎨 **Phase 4: フロントエンド開発** (3-4時間)
- [ ] Vite + React + TypeScript セットアップ
- [ ] Redux store設定
- [ ] Socket.IO クライアント設定
- [ ] 投票ルーム作成画面
- [ ] 投票参加画面
- [ ] リアルタイム結果表示画面
- [ ] Tailwind CSS スタイリング

## 🔗 **Phase 5: 統合・テスト** (1時間)
- [ ] フロントエンド・バックエンド連携テスト
- [ ] リアルタイム機能動作確認
- [ ] 複数ユーザーでの動作テスト
- [ ] レスポンシブ対応確認

## 🚀 **Phase 6: デプロイ準備** (30分)
- [ ] Dockerfile作成
- [ ] Heroku設定ファイル（Procfile）
- [ ] 環境変数設定
- [ ] 本番環境テスト

# 🎯 **MVP機能範囲**
- 投票ルーム作成（質問 + 選択肢）
- 投票ルーム参加（ルームコード入力）
- リアルタイム投票
- リアルタイム結果表示（棒グラフ）
- 投票終了機能

# ⏰ **時間配分目安**
- **午前** (4時間): Phase 1-3 完了
- **午後** (4時間): Phase 4-6 完了

# 🔧 **使用する主要技術**
- **バックエンド**: Flask + Flask-SocketIO + SQLAlchemy + Redis
- **フロントエンド**: React + TypeScript + Redux + Socket.IO + Tailwind CSS
- **データベース**: PostgreSQL
- **リアルタイム**: WebSocket (Socket.IO)
