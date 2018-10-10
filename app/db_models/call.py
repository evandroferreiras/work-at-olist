from app.core.db import db


class CallDetailType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)

    def __str__(self):
        return self.description


class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_phone = db.Column(db.String(11))
    destination_phone = db.Column(db.String(11))


class CallDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    detail_type_id = db.Column(
        db.Integer, db.ForeignKey('call_detail_type.id'), nullable=False)
    detail_type = db.relationship('CallDetailType')
    date_added = db.Column(db.DateTime, nullable=False)
    call_id = db.Column(
        db.Integer, db.ForeignKey('call.id'), nullable=False)
    call = db.relationship('Call')

    def __str__(self):
        return self.description
