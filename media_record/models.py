from media_record.db import Base
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key = True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    first_name = Column(String(50), )
    last_name = Column(String(50),)
    created_on = Column(DateTime, default=datetime.now())

    records = relationship('Record')

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'<User {self.username!r}>'
    
    def __str__(self):
        return f'<User {self.username!r}>'

class Record(Base):
    __tablename__ = 'records'

    record_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(120),nullable=False )
    media_type = Column(String(20), nullable=False)
    current_episode_non_season = Column(Integer, nullable=False, default=0)
    full_episode_non_season = Column(Integer, nullable=False, default=0)
    finished_airing = Column(Date)
    completion_rate = Column(Integer)

    def __init__(self, name, media_type, current_episode, full_episode):
        self.name = name
        self.media_type = media_type
        self.current_episode_non_season = current_episode
        self.full_episode_non_season = full_episode


if __name__ == "__main__":
    raise NotImplementedError