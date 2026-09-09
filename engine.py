import json
from main import Suggestion


class Priority_Engine:
    def __init__(self, storage_file="blackboxdata.json"):
        self.storage_file = storage_file
        self.suggestions = self.load_data()

    def load_data(self):
        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)
            loaded = []
            for item in data:
                item.setdefault("urgency", "MEDIUM")
                item.setdefault("reports", 1)
                item.setdefault("votes", 0)
                item.setdefault("affected", 1)
                item.setdefault("status", "Pending")
                item.setdefault("upvoted_by", [])
                loaded.append(Suggestion(**item))
            return loaded
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_suggestion(self):
        with open(self.storage_file, "w") as f:
            json.dump([s.to_dict() for s in self.suggestions], f, indent=4)

    def add_suggestion(self, text, category, location, affected):
        new_id = 1
        if self.suggestions:
            new_id = max(s.suggestion_id for s in self.suggestions) + 1

        new_issue = Suggestion(
            suggestion_id=new_id,
            text=text,
            category=category,
            location=location,
            urgency="MEDIUM",
            reports=1,
            votes=0,
            affected=affected,
        )
        self.suggestions.append(new_issue)
        self.save_suggestion()
        return f"Issue #{new_id} submitted successfully."

    def get_ranked_suggestions(self):
        return sorted(
            self.suggestions,
            key=lambda s: s.calc_priority_score(),
            reverse=True,
        )

    def update_status(self, issue_id, new_status):
        valid_statuses = [
            "Pending",
            "Under Review",
            "In Progress",
            "Resolved",
            "Rejected",
        ]
        if new_status not in valid_statuses:
            return False, "Invalid status"

        for issue in self.suggestions:
            if issue.suggestion_id == issue_id:

                if new_status == "Rejected":
                    self.suggestions.remove(issue)
                    self.save_suggestion()

                    return True,( f"Issue #{issue_id} was rejected and deleted."
                    )

                issue.status = new_status
                self.save_suggestion()

                return True, (
                    f"Issue #{issue_id} status changed to {new_status}."
                )

        return False, f"Issue #{issue_id} was not found."


