from db import *
from mimesis import Generic
from mimesis.enums import Gender
from random import choice

generator = Generic('ru').person


def time_gen():
    for h, m in ((9, 30), (11, 20), (13, 10), (15, 25), (17, 15)):
        session.add(Time(start_hour=h,
                         start_minute=m,
                         end_hour=h + (m + 95) // 60,
                         end_minute=(m + 95) % 60))


def day_gen():
    for i in range(12):
        session.add(Day(number_in_all=i,
                        number_in_week=i % 6,
                        number_of_week=i // 6))


def teacher_gen(c):
    for i in range(c):
        g = choice((Gender.FEMALE, Gender.MALE))
        session.add(Teacher(first_name=generator.name(gender=g),
                            last_name=generator.last_name(gender=g),
                            number=generator.telephone(),
                            hrefs=generator.social_media_profile(),
                            email=generator.email()))


def room_gen(c):
    for name in ('Народного Ополчения', 'Авиамоторная'):
        loc = Location(name=name)
        loc.rooms = [Room(name=str(i)) for i in range(c)]
        session.add(loc)


def group_gen(c):
    for i in range(c):
        session.add(Group(name=f'Группа №{i}'))


def generate():
    time_gen()
    day_gen()
    teacher_gen(10)
    room_gen(20)
    group_gen(10)


def create():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    generate()
    session.commit()


create()
