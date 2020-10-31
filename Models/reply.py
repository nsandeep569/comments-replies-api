from db import db
import datetime
from time import strftime
import time
from datetime import datetime


class ReplyModel(db.Model):
    __tablename__ = 'replies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    reply = db.Column(db.String(500))
    reply_timestamp = db.Column(db.String(30))
    reply_type = db.Column(db.String(1))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    comment_reply = db.relationship('CommentModel')
    parent_reply_id = db.Column(db.Integer, db.ForeignKey('replies.id'))
    replies_reply = db.relationship('ReplyModel')

    def __init__(self, comment_id, name, reply, reply_type, parent_reply_id):
        self.name = name
        self.reply = reply
        self.reply_timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.reply_type = reply_type
        self.comment_id = comment_id
        self.parent_reply_id = parent_reply_id

        # self.comment_timestamp = time.time()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'reply': self.reply,
            'reply_timestamp': self.reply_timestamp,
            'reply_type': self.reply_type,
            'comment_id': self.comment_id,
            'parent_reply_id': self.parent_reply_id

        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_reply_id(cls, reply_id):
        return cls.query.filter_by(id=reply_id).first()

    @classmethod
    def find_all_reply_id_using_parent_id(cls, parent_reply_id):
        return cls.query.filter_by(parent_reply_id=parent_reply_id).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
