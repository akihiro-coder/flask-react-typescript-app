from flask import Blueprint, request, jsonify
from app import db
from app.models import VotingRoom, VotingOption, Vote
from sqlalchemy.exc import IntegrityError

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/api/rooms', methods=['POST'])
def create_room():
    """投票ルーム作成"""
    try:
        data = request.get_json()

        # バリデーション
        if not data or not data.get('title'):
            return {'error': 'Title is required'}, 400

        if not data.get('options') or len(data.get('options')) < 2:
            return {'error': 'At least 2 options are required'}, 400

        # 投票ルーム作成
        room = VotingRoom(
            title=data['title'],
            description=data.get('description', '')
        )
        db.session.add(room)
        db.session.flush()  # IDを取得するため

        # 選択肢作成
        for i, option_text in enumerate(data['options']):
            if option_text.strip():  # 空文字列チェック
                option = VotingOption(
                    room_id=room.id,
                    text=option_text.strip(),
                    order=i
                )
                db.session.add(option)

        db.session.commit()

        return {
            'success': True,
            'room': room.to_dict()
        }, 201

    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to create room: {str(e)}'}, 500

@rooms_bp.route('/api/rooms/<room_code>', methods=['GET'])
def get_room(room_code):
    """投票ルーム取得"""
    try:
        room = VotingRoom.query.filter_by(room_code=room_code).first()

        if not room:
            return {'error': 'Room not found'}, 404

        if not room.is_active:
            return {'error': 'Room is closed'}, 410

        return {
            'success': True,
            'room': room.to_dict(),
            'results': room.get_results()
        }

    except Exception as e:
        return {'error': f'Failed to get room: {str(e)}'}, 500

@rooms_bp.route('/api/rooms/<room_code>/close', methods=['POST'])
def close_room(room_code):
    """投票ルーム終了"""
    try:
        room = VotingRoom.query.filter_by(room_code=room_code).first()

        if not room:
            return {'error': 'Room not found'}, 404

        room.is_active = False
        room.ended_at = db.func.now()
        db.session.commit()

        return {
            'success': True,
            'message': 'Room closed successfully'
        }

    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to close room: {str(e)}'}, 500
