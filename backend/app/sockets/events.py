from flask_socketio import emit, join_room, leave_room
from app import socketio
from app.models import VotingRoom

@socketio.on('join_room')
def handle_join_room(data):
    """投票ルームに参加"""
    try:
        room_code = data.get('room_code')

        if not room_code:
            emit('error', {'message': 'Room code is required'})
            return

        # ルーム存在確認
        room = VotingRoom.query.filter_by(room_code=room_code).first()
        if not room:
            emit('error', {'message': 'Room not found'})
            return

        # Socket.IOルームに参加
        join_room(room_code)

        # 現在の結果を送信
        emit('room_joined', {
            'room_code': room_code,
            'room': room.to_dict(),
            'results': room.get_results()
        })

        # 他の参加者に通知
        emit('user_joined', {
            'message': f'A user joined room {room_code}'
        }, room=room_code, include_self=False)

    except Exception as e:
        emit('error', {'message': f'Failed to join room: {str(e)}'})

@socketio.on('leave_room')
def handle_leave_room(data):
    """投票ルームから退出"""
    try:
        room_code = data.get('room_code')

        if room_code:
            leave_room(room_code)
            emit('user_left', {
                'message': f'A user left room {room_code}'
            }, room=room_code)

    except Exception as e:
        emit('error', {'message': f'Failed to leave room: {str(e)}'})

@socketio.on('connect')
def handle_connect():
    """クライアント接続"""
    emit('connected', {'message': 'Connected to voting server'})

@socketio.on('disconnect')
def handle_disconnect():
    """クライアント切断"""
    print('Client disconnected')
