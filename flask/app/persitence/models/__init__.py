from app.persitence.db import Document, db

ACCESS = {
    'guest': 0,
    'user': 1,
    'instructor': 2,
    'admin': 3
}


class User(Document):
    collection = db.users

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    def has_access(self, level):
        return ACCESS[self.access_level] >= ACCESS[level]


class Message(Document):
    collection = db.messages
