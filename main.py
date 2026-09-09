#user inheritance
class User:
    #base class for all users in this system
    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type
class Student(User):
    def __init__(self, username):
        super().__init__(username, user_type="student")
class Admin(User):
    def __init__(self, username):
        super().__init__(username, user_type="admin")

#suggestions
class Suggestion:
    def __init__(
            self,
            suggestion_id,
            text,
            category,
            location,
            urgency="MEDIUM",
            reports=1,
            votes=0,
            affected=1,
            status="Pending",
            upvoted_by=None
    ):
        self.suggestion_id = suggestion_id
        self.text = text
        self.category = category
        self.location = location
        self.urgency = urgency
        self.reports = int(reports)
        self.votes = int(votes)
        self.affected = int(affected)
        self.status = status
        self.upvoted_by = upvoted_by if upvoted_by is not None else []

    def calc_priority_score(self):
        return (self.reports * 2) + self.affected + self.votes

    def calc_priority_level(self):
        score = self.calc_priority_score()
        if score < 10:
            return "LOW"
        elif 10 <= score < 25:
            return "MEDIUM"
        else:
            return "HIGH"

    def to_dict(self):
        return self.__dict__

