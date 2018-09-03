import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Question as QuestionModel, Base
from utils import input_to_dictionary
from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
"""
  __tablename__='question'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    contents = Column(String(1000))
"""
class QuestionAttribute:
    uid = graphene.ID()
    did = graphene.ID()
    contents = graphene.String()

class Question(SQLAlchemyObjectType):
    class Meta:
        model = QuestionModel
        interfaces = (relay.Node, )


class CreateQuestionInput(graphene.InputObjectType,QuestionAttribute):
    pass


class CreateQuestion(graphene.Mutation):
    question = graphene.Field(lambda:Question)

    class Arguments:
        input = CreateQuestionInput(required=True)
    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['created'] = datetime.utcnow()
        data['edited'] = datetime.utcnow()
        question = QuestioneModel(**data)
        db_session.add(question)
        db_session.commit()
        #middleware 처리할
        return CreateQuestion(question=question)


class UpdateQuestionInput(graphene.InputObjectType, QuestionAttribute):
    """Arguments to update"""
    id = graphene.ID(required=True)


class UpdateQuestion(graphene.Mutation):
    """Update"""
    question = graphene.Field(lambda: Question, )

    class Arguments:
        input = UpdateQuestionInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        question = db_session.query(QuestionModel).filter_by(id=data['id'])
        question.update(data)
        db_session.commit()
        question = db_session.query(QuestionModel).filter_by(id=data['id']).first()

        return UpdateQuestion(question=question)