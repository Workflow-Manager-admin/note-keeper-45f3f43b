import uuid
from datetime import datetime

# PUBLIC_INTERFACE
class Note:
    """A Note data object with id, title, content, and timestamp."""
    def __init__(self, title, content, id=None, timestamp=None):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(data):
        return Note(
            id=data.get("id"),
            title=data["title"],
            content=data["content"],
            timestamp=data.get("timestamp"),
        )
