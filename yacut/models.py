from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(2048), nullable=False)
    short = db.Column(db.String(16), unique=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<URLMap {self.original} -> {self.short}>'

    def from_dict(self, data):
        for field in ('original', 'short'):
            if field in data:
                setattr(self, field, data[field])
