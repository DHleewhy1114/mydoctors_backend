import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, User as UserModel,Doctor as DoctorModel, Hospital as HospitalModel, Message as MessageModel, Messagerecipient as MessagerecipientModel, \
Relationship as RelationshipModel, Schedule as ScheduleModel
from schema_user import CreateUser, User
from schema_doctor import CreateDoctor, Doctor
from schema_hospital import CreateHospital, Hospital
from schema_message import CreateMessage, Message
from schema_messagerecipient import CreateMessagerecipient, Messagerecipient
from schema_relationship import CreateRelationship, Relationship
from schema_schedule import CreateSchedule, Schedule
"""
from schema_category import CreateCatgory, Category
from schema_quest import CreateQuest, Quest
from schema_process import CreateProcess, Process
"""
"""
class Category(SQLAlchemyObjectType):
    class Meta:
        model = CategoryModel
        interfaces = (relay.Node, )

class Comment(SQLAlchemyObjectType):
    class Meta:
        model = CommentModel
        interfaces = (relay.Node, )
"""
class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_doctor = CreateDoctor.Field()
    create_message = CreateMessage.Field()
    create_relationship = CreateRelationship.Field()
    create_schedule = CreateSchedule.Field()
    create_hospital = CreateHospital.Field()

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user = relay.Node.Field(User)
    userlist = SQLAlchemyConnectionField(User)
    doctor = relay.Node.Field(Doctor)
    doctorlist = SQLAlchemyConnectionField(Doctor)
    messagelist = SQLAlchemyConnectionField(Message)
    schedule = relay.Node.Field(Schedule)
    schedulelist = SQLAlchemyConnectionField(Schedule)



"""
수정 및 삭제 쿼리 만들것
"""


"""  node = graphene.relay.Node.Field()
    people = graphene.relay.Node.Field(schema_people.People)
    peopleList = SQLAlchemyConnectionField(schema_people.People)
    planet = graphene.relay.Node.Field(schema_planet.Planet)
    planetList = SQLAlchemyConnectionField(schema_planet.Planet
"""
schema = graphene.Schema(query=Query,mutation=Mutations)

