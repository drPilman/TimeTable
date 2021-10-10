from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.associationproxy import association_proxy
import json
from db.connection import DB_URL

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

    def __repr__(self):
        return f'{self.id}  {self.start_hour}'


class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True)
    number_in_all = Column(Integer, nullable=False)
    number_in_week = Column(Integer, nullable=False)
    number_of_week = Column(Integer, nullable=False)
    # name = Column(String, nullable=False)
    lessons = relationship('Lesson', cascade='all,delete', back_populates='day')


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    comment = Column(String)
    lessons = relationship('Lesson', cascade='all,delete', back_populates='group')

    def __repr__(self):
        return f"{self.id}: {self.name}"


class Type(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lessons = relationship('Lesson', cascade='all,delete', back_populates='type')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    short = Column(String, nullable=False)
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

    def name(self):
        return f'{self.second_name} {self.first_name[0] + "." if self.first_name else ""}'


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
    type_id = Column(Integer, ForeignKey('types.id'))
    type = relationship('Type', back_populates='lessons')
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship('Teacher', back_populates='lessons')
    room_id = Column(Integer, ForeignKey('rooms.id'))
    room = relationship('Room', back_populates='lessons')
    comment = Column(String)

    def __repr__(self):
        return f'{self.subject.name} {self.group.name} {self.time_id}'


def getWeekById(group_id, week_num):
    res = [[('') * 3 for les in range(5)] for day in range(5)]
    for lesson in session.query(Lesson.time_id,
                                Subject.short,
                                Day.number_in_week,
                                Room.name.label('room'),
                                Teacher.second_name,
                                Teacher.first_name,
                                Type.name) \
            .join(Lesson.day) \
            .join(Lesson.teacher) \
            .join(Lesson.room) \
            .join(Lesson.subject) \
            .join(Lesson.type) \
            .filter(Day.number_of_week == week_num) \
            .filter(Lesson.group_id == group_id).all():
        res[lesson.number_in_week][lesson.time_id - 1] = \
            lesson.short,\
            lesson.name,\
            lesson.room, \
            Teacher.name(lesson)
    return res


def getTime():
    return [f'{s.start_hour}:{s.start_minute} - {s.end_hour}:{s.end_minute}' for s in
            session.query(Time).order_by(Time.id).all()]


def getGroupList():
    return session.query(Group).all()