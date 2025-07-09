from datetime import datetime
from app import db

class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('voting_rooms.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('voting_options.id'), nullable=False)
    voter_session = db.Column(db.String(100), nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 複合ユニーク制約（同じルームで同じセッションは1票のみ）
    __table_args__ = (db.UniqueConstraint('room_id', 'voter_session', name='unique_vote_per_session'),)

    def __init__(self, room_id, option_id, voter_session):
        self.room_id = room_id
        self.option_id = option_id
        self.voter_session = voter_session

    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'option_id': self.option_id,
            'voted_at': self.voted_at.isoformat() if self.voted_at else None
        }
