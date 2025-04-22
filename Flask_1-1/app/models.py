from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import pytz  # 引入 pytz

@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    activities = db.relationship('Activity', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    participations = db.relationship('Participation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic', cascade='all, delete-orphan')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic', cascade='all, delete-orphan')

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.UTC))  # 显式指定 UTC
    event_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(100), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)
    participants = db.relationship('Participation', backref='activity', lazy='dynamic', cascade='all, delete-orphan')
    messages = db.relationship('Message', backref='activity', lazy='dynamic', cascade='all, delete-orphan')

class Participation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.UTC))  # 显式指定 UTC


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id', ondelete='CASCADE'), nullable=False)
    conversation_id = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.UTC))  # 显式指定 UTC

class Client(UserMixin,db.Model):
    __tablename__ = 'client'
    c_id = db.Column(db.CHAR(8), primary_key=True)
    c_usename = db.Column(db.CHAR(20), nullable=False)
    c_password = db.Column(db.CHAR(10), nullable=False)
    c_phonenumber = db.Column(db.CHAR(13))
    c_score = db.Column(db.CHAR(5))
    c_avatar_URL = db.Column(db.CHAR(255))  # 用户头像地址
    email = db.Column(db.String(120), unique=True, nullable=False)

    def get_id(self):
        return self.c_id

class Tags(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.CHAR(8), primary_key=True)
    tag_name = db.Column(db.CHAR(20), nullable=False)
    tag_desc = db.Column(db.CHAR(100))

class Activities(db.Model):
    __tablename__ = 'activities'
    a_id = db.Column(db.CHAR(8), primary_key=True)
    a_name = db.Column(db.CHAR(255), nullable=False)
    a_text = db.Column(db.Text)  # 活动详细介绍文本存储地址
    a_image_url = db.Column(db.CHAR(255))  # 活动图片存储地址
    a_location = db.Column(db.Text)  # 活动地点
    creator_c_id = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'))
    limit_p = db.Column(db.Integer)  # 参与人数限制
    activity_status = db.Column(db.VARCHAR(50))  # 活动状态
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.UTC))  # 显式指定 UTC
    event_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    creator = db.relationship('Client', foreign_keys=[creator_c_id])

class ActivityParticipation(db.Model):
    __tablename__ = 'activity_participation'
    a_id = db.Column(db.CHAR(8), db.ForeignKey('activities.a_id'), primary_key=True)
    participant_c_id = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'), primary_key=True)
    creator_c_id = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'))
    participant = db.relationship('Client', foreign_keys=[participant_c_id])
    creator = db.relationship('Client', foreign_keys=[creator_c_id])

class Evaluations(db.Model):
    __tablename__ = 'evaluations'
    e_id = db.Column(db.CHAR(8), primary_key=True)
    user_id = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'), nullable=False)  # 评价用户id
    a_id = db.Column(db.CHAR(8), db.ForeignKey('activities.a_id'))  # 评价活动id
    evaluation_content = db.Column(db.CHAR(255))  # 评价内容
    e_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())  # 评价时间
    rating = db.Column(db.Integer)  # 评分
    e_type = db.Column(db.VARCHAR(50))  # 评价类型
    user = db.relationship('Client', foreign_keys=[user_id])

class FriendRelationships(db.Model):
    __tablename__ = 'friend_relationships'
    user_id1 = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'), primary_key=True)
    user_id2 = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'), primary_key=True)
    friend1 = db.relationship('Client', foreign_keys=[user_id1])
    friend2 = db.relationship('Client',foreign_keys=[user_id2])
    relationship_status = db.Column(db.CHAR(50))



class Hobby(db.Model):
    __tablename__ = 'hobby'
    c_id = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'), primary_key=True)
    tag_id = db.Column(db.CHAR(8), db.ForeignKey('tags.tag_id'), primary_key=True)

class ChatRecords(db.Model):
    __tablename__ = 'chat_records'
    message_id = db.Column(db.CHAR(8), primary_key=True)
    sender_c_id = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'))
    receiver_c_id = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'))
    message_content = db.Column(db.CHAR(255))
    send_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    activity_id = db.Column(db.CHAR(8), db.ForeignKey('activities.a_id'), nullable=False)
    conversation_id = db.Column(db.String(100), nullable=False)
    sender = db.relationship('Client',foreign_keys=[sender_c_id])
    receiver = db.relationship('Client',foreign_keys=[receiver_c_id])

class ActivityTag(db.Model):
    __tablename__ = 'activity_tag_association'
    a_id = db.Column(db.CHAR(8), db.ForeignKey('activities.a_id'), primary_key=True)
    tag_id = db.Column(db.CHAR(8), db.ForeignKey('tags.tag_id'), primary_key=True)
    tag = db.relationship('Tags',foreign_keys=[tag_id])

class Group(db.Model):
    __tablename__ = 'groups'
    g_id = db.Column(db.CHAR(8), primary_key=True)
    g_name = db.Column(db.String(255), nullable=False)
    creator_id = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'))
    creator = db.relationship('Client',foreign_keys=[creator_id])

class GroupMembers(db.Model):
    __tablename__ = 'group_members'
    m_id = db.Column(db.CHAR(8), primary_key=True)
    g_id = db.Column(db.CHAR(8), db.ForeignKey('groups.g_id'))
    c_id = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'))
    group= db.relationship('Group',foreign_keys=[g_id])

class GroupRecords(db.Model):
    __tablename__ = 'group_records'
    message_id = db.Column(db.CHAR(8), primary_key=True)
    sender_c_id = db.Column(db.CHAR(8), db.ForeignKey('client.c_id'))
    g_id = db.Column(db.CHAR(8), db.ForeignKey('groups.g_id'))
    chat_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    chat_content = db.Column(db.Text)
    sender=db.relationship('Client',foreign_keys=[sender_c_id])

