from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(80))
    description=db.Column(db.String(100))
    completed_at=db.Column(db.DateTime,nullable=True)
    
    def to_dict(self):
        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at is not None
            }