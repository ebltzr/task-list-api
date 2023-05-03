from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    description=db.Column(db.String(100))
    completed_at=db.Column(db.DateTime,nullable=True)