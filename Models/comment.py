from db import db
import datetime
from time import strftime
import time
from datetime import datetime


class CommentModel(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    comment = db.Column(db.String(500))
    # comment_timestamp = db.Column(db.DateTime()) not supporting in sqllite3
    #comment_timestamp = db.Column(db.Float(precision=10))
    comment_timestamp = db.Column(db.String(30))
    comment_replies = db.relationship(
        'ReplyModel',
        # backref=db.backref('replies', uselist=True),
        lazy='dynamic')

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment
        # self.comment_timestamp = datetime.datetime.now()
        # print(strftime('%s', 'now'))
        # self.comment_timestamp = strftime('%s', 'now')
        self.comment_timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        # self.comment_timestamp = time.time()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'comment': self.comment,
            # 'comment_timestamp': (datetime.datetime.now() + datetime.timedelta(microseconds=self.comment_timestamp/10)).strftime("%Y-%m-%d %H:%M:%S")
            'comment_timestamp': self.comment_timestamp,
            'replies': [reply.json() for reply in self.comment_replies.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_comment_id(cls, comment_id):
        return cls.query.filter_by(id=comment_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
