from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash
#from sqlalchemy_imageattach.entity import Image,image_attachment
engine = create_engine('mysql://mydoc:mydoc@localhost/mydoc', convert_unicode=True)
db_session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))

Base = declarative_base()
Base.metadata.bind = engine
Base.query = db_session.query_property()

class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password_hash = Column(String(256))
    created = Column(String(50))
    edited = Column(String(50))
    #isdoctor = Column(Boolean)
    #hospital_id = Column(Integer,ForeignKey('hospital.id'),nullable=False)
    #profile_photo = Column(String(129))
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        #self.password_hash = generate_password_hash(password)
        self.password_hash = password

class Doctor(Base):
    __tablename__='doctor'
    id = Column(Integer, primary_key=True)
    doctor_name = Column(String(64), index=True)
    doctor_code = Column(Integer,index = True)
    hospital_id = Column(Integer,ForeignKey('hospital.id'),nullable=false)
    #doctor_info = Column(String(50))
    created = Column(String(50))
    edited = Column(String(50))
    #profile_photo = Column(String(129))

class Hospital(Base):
    #api를 통해 좌표 받아오기
    __tablename__='hospital'
    id = Column(Integer, primary_key=True)
    hospital_name = Column(String(1000))
    position_x = Column(Integer)
    position_y = Column(Integer)
    created = Column(String(50))
    edited = Column(String(50))
    doctorList = relationship(Doctor, backref='doctor')

class Relationship(Base):
    __tablename__='relationship'
    id = Column(Integer,primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    created = Column(String(50))
    edited = Column(String(50))

    def mydoctor_id(self):
        return [self.did]

class Schedule(Base):
    __tablename__='schedule'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    time = Column(String(50))
    created = Column(String(50))
    edited = Column(String(50))
    question_id = Column(Integer,ForeignKey('question.id'),nullable=True)

class Answer(Base):
    __tablename__='answer'
    id = Column(Integer, primary_key=True)
    #uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    #did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    question_id = Column(Integer,ForeignKey('question.id'),nullable=False)
    contents = Column(String(1000))
    created = Column(String(50))
    edited = Column(String(50))
    #schedule_id = Column(Integer,ForeignKey('schedule.id'),nullable=False)

class Question(Base):
    __tablename__='question'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    contents = Column(String(1000))
    created = Column(String(50))
    edited = Column(String(50))
    answerList = relationship(Answer, backref='answer')
    #profile_photo = Column(String(129))
