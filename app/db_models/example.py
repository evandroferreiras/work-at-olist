from app import app
from app.core.db import db


class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)

    def __str__(self):
        return self.description

    @staticmethod
    def get_by_id(id):
        with app.app_context():
            return db.session.query(Example).filter_by(
                id=id).one()
