from flask import Blueprint, request, jsonify
from app import db, socketio
from app.models import VotingRoom, VotingOption, Vote
from sqlalchemy.exc import IntegrityError
import uuid

votes_bp = Blueprint('votes', __name__)

@votes_bp.route('/api/vote', methods=['POST'])
def cast_vote():
    """投票実行"""
    try:
        data = request.get_json()

        # バリデーション
        required_fields = ['room_code', 'option_id', 'voter_session']
        for field in required_fields:
            if not data or not data.get(field):
                return {'error': f'{field} is required'}, 400

        room_code = data['room_code']
        option_id = data['option_id']
        voter_session = data['voter_session']

        # ルーム存在確認
        room = VotingRoom.query.filter_by(room_code=room_code).first()
        if not room:
            return {'error': 'Room not found'}, 404

        if not room.is_active:
            return {'error': 'Room is closed'}, 410

        # 選択肢存在確認
        option = VotingOption.query.filter_by(id=option_id, room_id=room.id).first()
        if not option:
            return {'error': 'Invalid option'}, 400

        # 重複投票チェック
        existing_vote = Vote.query.filter_by(
            room_id=room.id,
            voter_session=voter_session
        ).first()

        if existing_vote:
            return {'error': 'You have already voted in this room'}, 409

        # 投票記録
        vote = Vote(
            room_id=room.id,
            option_id=option_id,
            voter_session=voter_session
        )
        db.session.add(vote)
        db.session.commit()

        # リアルタイム結果配信
        results = room.get_results()
        socketio.emit('vote_update', {
            'room_code': room_code,
            'results': results,
            'total_votes': len(room.votes)
        }, room=room_code)

        return {
            'success': True,
            'message': 'Vote cast successfully',
            'results': results
        }

    except IntegrityError:
        db.session.rollback()
        return {'error': 'You have already voted in this room'}, 409
    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to cast vote: {str(e)}'}, 500

@votes_bp.route('/api/rooms/<room_code>/results', methods=['GET'])
def get_results(room_code):
    """投票結果取得"""
    try:
        room = VotingRoom.query.filter_by(room_code=room_code).first()

        if not room:
            return {'error': 'Room not found'}, 404

        return {
            'success': True,
            'room_code': room_code,
            'results': room.get_results(),
            'total_votes': len(room.votes),
            'is_active': room.is_active
        }

    except Exception as e:
        return {'error': f'Failed to get results: {str(e)}'}, 500

@votes_bp.route('/api/session', methods=['GET'])
def get_session():
    """新しいセッションIDを生成"""
    session_id = f"session_{uuid.uuid4().hex[:12]}"
    return {
        'success': True,
        'session_id': session_id
    }
