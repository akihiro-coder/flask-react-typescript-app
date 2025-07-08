from app import db

class VotingOption(db.Model):
    __tablename__ = 'voting_options'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('voting_rooms.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    order = db.Column(db.Integer, default=0)

    # リレーション
    votes = db.relationship('Vote', backref='option', lazy=True, cascade='all, delete-orphan')

    def __init__(self, room_id, text, order=0):
        self.room_id = room_id
        self.text = text
        self.order = order

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'order': self.order,
            'vote_count': len(self.votes)
        }
