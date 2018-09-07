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
import base64
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
    #userlist = SQLAlchemyConnectionField(User)
    find_user = graphene.List(lambda: User, username = graphene.String())
    doctor = relay.Node.Field(Doctor)
    doctorlist = SQLAlchemyConnectionField(Doctor)
    mydoctors = graphene.List(lambda:Doctor,id=graphene.String())
    #mydoctorslist =  graphene.List(lambda:Doctor,did=graphene.String())
    find_doctor = graphene.List(lambda:Doctor,doctor_name=graphene.String())
    find_doctor_by_code = graphene.Field(lambda:Doctor,doctor_code=graphene.Int())
    question = relay.Node.Field(Question)
    questionlist = SQLAlchemyConnectionField(Question)
    question_by_user = graphene.List(lambda:Question,uid=graphene.ID(),did=graphene.ID())
    relationship = relay.Node.Field(Relationship)
    relationshiplist = SQLAlchemyConnectionField(Relationship)
    answer = relay.Node.Field(Answer)
    #answerlist = SQLAlchemyConnectionField(Answer)
    answer_by_question = graphene.List(lambda:Answer,question_id=graphene.ID())
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
    
    def resolve_find_doctor_by_code(self,info,doctor_code):
        query = Doctor.get_query(info)
        print ("codequery")
        print (query.filter(DoctorModel.doctor_code == doctor_code).first())
        return query.filter(DoctorModel.doctor_code == doctor_code).first()
    
    def resolve_find_hospital(self,info,hospital_name):
        query = Hospital.get_query(info)
        return query.filter(HospitalModel.hospital_name == hospital_name).all()
        
    def resolve_question_by_user(self,info,uid,did):
        query = Question.get_query(info)
        uid = base64.b64decode(uid)
        did = base64.b64decode(did)
        int_uid = int(str(uid)[7:-1])
        int_did = int(str(did)[9:-1])
        print (int_did)
        return query.filter(QuestionModel.uid == int_uid).filter(QuestionModel.did == int_did).all()
    
    def resolve_answer_by_question(self,info,question_id):
        query = Answer.get_query(info)
        question_id = base64.b64decode(question_id)
        int_question_id = int(str(question_id)[11:-1])
        print (int_question_id)
        return query.filter(AnswerModel.question_id == int_question_id).all()

    def resolve_mydoctors(self,info,id):
        """query {
  mydoctors(id:"VXNlcjox"==user_id){
    doctorName
    doctorCode
    }
}       """
        mydoctors_list=[]
        query = Relationship.get_query(info)
        doctor_query=Doctor.get_query(info)
        user_id = base64.b64decode(id)
        int_user_id =int(str(user_id)[7:-1])
        for item in query.filter(RelationshipModel.uid==int_user_id).all():
            print (doctor_query.filter(DoctorModel.id == item.__dict__['did'] ).first())
            mydoctors_list+=[doctor_query.filter(DoctorModel.id == item.__dict__['did']).first()]
        return mydoctors_list
        
"""
수정 및 삭제 쿼리 만들것
"""
"""
query{
  mydoctors(uid:"VXNlcjox"){
   doctor{
    doctorList{
      edges{
        node{
          doctorName
          doctorCode
        }
      }
    }
  }
  }
}
{
  "data": {
    "createRelationship": {
      "relationship": {
        "id": "UmVsYXRpb25zaGlwOjI=",
        "uid": 1,
        "did": 1
      }
    }
  }
}
"""
schema = graphene.Schema(query=Query,mutation=Mutations)


