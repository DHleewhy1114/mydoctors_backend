import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, User as UserModel,Doctor as DoctorModel, Hospital as HospitalModel, \
Question as QuestionModel, Answer as AnswerModel, Relationship as RelationshipModel, Schedule as ScheduleModel
from schema_user import CreateUser, User
from schema_doctor import CreateDoctor, Doctor
from schema_hospital import CreateHospital, Hospital
from schema_question import CreateQuestion, Question
from schema_answer import CreateAnswer, Answer
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
    create_question = CreateQuestion.Field()
    create_answer = CreateAnswer.Field()
    create_relationship = CreateRelationship.Field()
    create_schedule = CreateSchedule.Field()
    create_hospital = CreateHospital.Field()

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user = relay.Node.Field(User)
    userlist = SQLAlchemyConnectionField(User)
    find_user = graphene.List(lambda: User, username = graphene.String())
    doctor = relay.Node.Field(Doctor)
    doctorlist = SQLAlchemyConnectionField(Doctor)
    find_doctor = graphene.List(lambda:Doctor,doctor_name=graphene.String())
    find_doctor_by_code = graphene.Field(lambda:Doctor,doctor_code=graphene.Int())
    question = relay.Node.Field(Question)
    questionlist = SQLAlchemyConnectionField(Question)
    relationship = relay.Node.Field(Relationship)
    relationshiplist = SQLAlchemyConnectionField(Relationship)
    answer = relay.Node.Field(Answer)
    answerlist = SQLAlchemyConnectionField(Answer)
    hospital = relay.Node.Field(Hospital)
    hospitallist = SQLAlchemyConnectionField(Hospital)
    find_hospital = graphene.List(lambda:Hospital,hospital_name=graphene.String())
    schedule = relay.Node.Field(Schedule)
    schedulelist = SQLAlchemyConnectionField(Schedule)

    def resolve_find_user(self,info,username):
        query = User.get_query(info)
        #username = args.get('username')
		# you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
        return query.filter(UserModel.username == username).all()

    def resolve_find_doctor(self,info,doctor_name):
        query = Doctor.get_query(info)
        #print (query)
        #print (query.filter(DoctorModel.doctor_name == doctor_name).first())
        #User.query.order_by(User.username).all()
        #안되는 이유는 리스트 객체라 어려운거 같음
        print (query.filter(DoctorModel.doctor_name == doctor_name).all())
        return query.filter(DoctorModel.doctor_name == doctor_name).all()
        #(DoctorModel.doctor_name == doctor_name).all()#filter의 all이 안먹
    
    def resolve_find_doctor_by_code(self,info,doctor_code):
        query = Doctor.get_query(info)
        return query.filter(DoctorModel.doctor_code == doctor_code).first()
    
    def resolve_find_hospital(self,info,hospital_name):
        query = Hospital.get_query(info)
        return query.filter(HospitalModel.hospital_name == hospital_name).all()
        
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


