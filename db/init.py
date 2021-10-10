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


"инф.тех."
"комп.граф."
"инф.экология"
"физ-ра"
"выш.мат."
"алгем"
"ин.яз."
"выч.тех."
"философия"
raspis = ((
              ('инф.тех.|2|ВЦ127|11', 'выч.тех.|3|314|12',
               'ин.яз.|2|404,301б|19',
               'комп.граф.|2|223|16', ''),
              ('физ-ра|4||17', 'философия|2|318|21', '', '', ''),
              (
                  '', '', '', 'инф.тех.|2|ВЦ116|11',
                  'инф.тех.|2|ВЦ116|11'),
              ('инф.экология|1|347|18', 'выч.тех.|1|310|20',
               'комп.граф.|1|126|15', '', ''),
              ('', 'инф.экология|3|339|18', 'выш.мат.|2|504а|13',
               'физ-ра|4||17',
               'алгем|2|508|14'),
          ),
          (
              ('инф.тех.|2|ВЦ127|11', 'выч.тех.|2|314|12',
               'ин.яз.|2|404,301б|19',
               'комп.граф.|2|223|16', ''),
              ('физ-ра|4||17', 'философия|2|318|21', '', '', ''),
              ('выш.мат.|1|522|13', 'алгем|1|347|14',
               'инф.тех.|1|517|11', '', ''),
              ('философия|1|514|21', 'выч.тех.|1|310|20', '', '', ''),
              ('', '', 'выш.мат.|2|504а|13', 'физ-ра|4||17',
               'алгем|2|508|14'),
          )
)


def gen():
    for weekn, t in enumerate(raspis):
        for dayn, d in enumerate(t):
            for timen, s in enumerate(d):
                if s:
                    subj, type_id, room, teacher_id = s.split('|')
                    subj_id = session.query(Subject.id).filter_by(short=subj).one()[0]
                    room_id = session.query(Room.id).filter_by(name=room).one()[0]
                    session.add(Lesson(group_id=11,
                                       time_id=timen + 1,
                                       day_id=weekn * 6 + dayn + 1,
                                       subject_id=subj_id,
                                       type_id=type_id,
                                       teacher_id=teacher_id,
                                       room_id=room_id))
    session.commit()


if __name__ == '__main__':
    pass
    #gen()
    # create()
