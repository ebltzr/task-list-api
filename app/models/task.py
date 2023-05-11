from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(80))
    description=db.Column(db.String(100))
    completed_at=db.Column(db.DateTime,nullable=True)
    
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    
    def to_dict(self):
        if self.goal_id:
            return{
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at is not None,
                "goal_id": self.goal_id
            }
        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at is not None,
            }
        
    @classmethod
    def from_dict(cls, request_data):
        new_task = Task(title=request_data["title"],
                        description=request_data["description"])
        return new_task