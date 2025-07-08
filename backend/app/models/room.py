from datetime import datetime
from app import db
import string
import random

class VotingRoom(db.Model):
    __tablename__ = 'voting_rooms'

    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String(6), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)

    # リレーション
    options = db.relationship('VotingOption', backref='room', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='room', lazy=True, cascade='all, delete-orphan')

    def __init__(self, title, description=None):
        self.title = title
        self.description = description
        self.room_code = self.generate_room_code()

    @staticmethod
    def generate_room_code():
        """6桁のランダムなルームコードを生成"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not VotingRoom.query.filter_by(room_code=code).first():
                return code

    def to_dict(self):
        return {
            'id': self.id,
            'room_code': self.room_code,
            'title': self.title,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'options': [option.to_dict() for option in self.options],
            'total_votes': len(self.votes)
        }

    def get_results(self):
        """投票結果を取得"""
        results = []
        for option in self.options:
            results.append({
                'option_id': option.id,
                'text': option.text,
                'vote_count': len(option.votes),
                'percentage': round((len(option.votes) / max(len(self.votes), 1)) * 100, 1)
            })
        return results
