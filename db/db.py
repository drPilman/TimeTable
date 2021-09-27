from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Session
import json
from connection import DB_URL

Base = declarative_base()
engine = create_engine(DB_URL, json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False))
session = Session(engine, future=True)


class Time(Base):
    __tablename__ = 'times'
    id = Column(Integer, primary_key=True)
    start_hour = Column(Integer, nullable=False)
    start_minute = Column(Integer, nullable=False, default=0)
    end_hour = Column(Integer, nullable=False)
    end_minute = Column(Integer, nullable=False, default=0)
    lessons = relationship('Lesson', cascade='all,delete', back_populates='time')


class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True)
    number_in_all = Column(Integer, nullable=False)
    number_in_week = Column(Integer, nullable=False)
    number_of_week = Column(Integer, nullable=False)
    #name = Column(String, nullable=False)
    lessons = relationship('Lesson', cascade='all,delete', back_populates='day')


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    comment = Column(String)
    lessons = relationship('Lesson', cascade='all,delete', back_populates='group')


class Type(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lessons = relationship('Lesson', cascade='all,delete', back_populates='type')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lessons = relationship('Lesson', cascade='all,delete', back_populates='subject')


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    comment = Column(String)
    rooms = relationship('Room', cascade='all,delete', back_populates='location')


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    comment = Column(String)
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship('Location', back_populates='rooms')
    lessons = relationship('Lesson', cascade='all,delete', back_populates='room')

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    second_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    number = Column(String)
    hrefs = Column(String)
    comment = Column(String)
    lessons = relationship('Lesson', cascade='all,delete', back_populates='teacher')


class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group', back_populates='lessons')
    time_id = Column(Integer, ForeignKey('times.id'), nullable=False)
    time = relationship('Time', back_populates='lessons')
    day_id = Column(Integer, ForeignKey('days.id'), nullable=False)
    day = relationship('Day', back_populates='lessons')
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    subject = relationship('Subject', back_populates='lessons')
    type_id = Column(Integer, ForeignKey('types.id'), nullable=False)
    type = relationship('Type', back_populates='lessons')
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher = relationship('Teacher', back_populates='lessons')
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    room = relationship('Room', back_populates='lessons')
    comment = Column(String)


"""
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    updatedAt = Column(DateTime, nullable=True, default=None)  # datetime.datetime.utcnow
    data = Column(JSON)  # nullable=True, default=None)
    isProcessed = Column(Boolean, nullable=False, default=False)
    timetables = relationship('Timetable')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    timetables = relationship('Timetable')


class Timetable(Base):
    __tablename__ = 'timetables'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))"""
