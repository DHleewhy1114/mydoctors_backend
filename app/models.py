from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash

engine = create_engine('mysql://quest:mission@localhost/QUEST', convert_unicode=True)
db_session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))

Base = declarative_base()
Base.metadata.bind = engine
Base.query = db_session.query_property()
"""

            Session = scoped_session(sessionmaker())

            class MyClass(object):
                query = Session.query_property()

            # after mappers are defined
            result = MyClass.query.filter(MyClass.name=='foo').all()

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        Department,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all'))

"""
class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password_hash = Column(String(256))
    created = Column(String(50))
    edited = Column(String(50))
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        #self.password_hash = generate_password_hash(password)
        self.password_hash = password

class Doctor(Base):
    __tablename__='doctor'
    id = Column(Integer, primary_key=True)
    doctorname = Column(String(64), index=True)
    hospital_id = Column(Integer,ForeignKey('hospital.id'),nullable=False)

class Hospital(Base):
    __tablename__='hospital'
    id = Column(Integer, primary_key=True)
    Hospitalname = Column(String(1000))
    position_x = Column(Integer)
    position_y = Column(Integer)
    
class Relationship(Base):
    __tablename__='relationship'
    id = Column(Integer,primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)

class Schedule(Base):
    __tablename__='schedule'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    content = Column(String(1000))
    time_from = Column(datetime)
    time_to = Column(datetime)

class Message(Base):
    __tablename__='message'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    parent_id = Column(Integer,ForeignKey('question.id'),nullable=True)
    content = Column(String(1000))

class Messagerecipient(Base):
    __tablename__='messagerecipient'
    id = Column(Integer, primary_key=True)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    message_id = Column(Integer, ForeignKey('message.id'), nullable=False)

"""
class Category(Base):
    __tablename__='category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(64),index=True)

class Quest(Base):
    __tablename__='quest'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(50))
    content = Column(String(1000))
    denied = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    created = Column(String(50))
    edited = Column(String(50))

class Process(Base):
    __tablename__='process'
    id = Column(Integer, primary_key=True)
    denied = Column(Boolean)
    quest_id = Column(Integer, ForeignKey('quest.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created = Column(String(50))
    edited = Column(String(50))
"""