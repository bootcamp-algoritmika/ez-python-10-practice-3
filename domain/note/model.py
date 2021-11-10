from typing import List


class Note:
    def __init__(self, header: str, likes: int, text: str, comments: int, color: int, tags: List[str], author: str,
                 created_date: str, modified_date: str = None, id: int = None):
        self.id: int = id
        self.header: str = header
        self.text: str = text
        self.tags: List[str] = tags
        self.author: str = author
        self.likes: int = likes
        self.comments: int = comments
        self.color: int = color
        self.created_date: str = created_date
        self.modified_date: str = modified_date
