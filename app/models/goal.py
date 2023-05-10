from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))

    def to_dict(self):
        return {
                "id": self.goal_id,
                "title": self.title
            }