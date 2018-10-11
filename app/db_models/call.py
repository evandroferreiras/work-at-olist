from app.core.db import db


class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_phone = db.Column(db.String(11))
    destination_phone = db.Column(db.String(11))
    started_date = db.Column(db.DateTime, nullable=False)
    finished_date = db.Column(db.DateTime, nullable=True)
    call_identifier = db.Column(db.Integer, unique=True)
