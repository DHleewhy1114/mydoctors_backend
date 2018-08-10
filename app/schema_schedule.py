import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Schedule as ScheduleModel, Base
from utils import input_to_dictionary
from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
"""
   class Schedule(Base):
    __tablename__='schedule'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    content = Column(String(1000))
    time_from = Column(datetime)
    time_to = Column(datetime)

"""
class ScheduleAttribute:
    uid = graphene.ID()
    did = graphene.ID()
    content = graphene.String()
    time_from = graphene.datetime()
    time_to = graphene.datetime()

class Schedule(SQLAlchemyObjectType):
    class Meta:
        model = ScheduleModel
        interfaces = (relay.Node, )

class CreateScheduleInput(graphene.InputObjectType, ScheduleAttribute):
    pass

class CreateSchedule(graphene.Mutation):
    schedule = graphene.Field(lambda:Schedule)

    class Arguments:
        input = CreateScheduleInput(required=True)
    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['created'] = datetime.utcnow()
        data['edited'] = datetime.utcnow()
        schedule = ScheduleModel(**data)
        db_session.add(schedule)
        db_session.commit()
        return CreateSchedule(schedule=schedule)


class UpdateScheduleInput(graphene.InputObjectType, ScheduleAttribute):
    """Arguments to update"""
    id = graphene.ID(required=True)


class UpdateSchedule(graphene.Mutation):
    """Update"""
    schedule = graphene.Field(lambda: Schedule, )

    class Arguments:
        input = UpdateScheduleInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        schedule = db_session.query(ScheduleModel).filter_by(id=data['id'])
        schedule.update(data)
        db_session.commit()
        schedule = db_session.query(ScheduleModel).filter_by(id=data['id']).first()

        return UpdateSchedule(schedule=schedule)
