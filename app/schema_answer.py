import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Answer as AnswerModel, Base
from utils import input_to_dictionary
from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
"""
 class Answer(Base):
    __tablename__='answer'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    question_id = Column(Integer,ForeignKey('question.id'),nullable=False)
    contents = Column(String(1000))
    created = Column(String(50))
    edited = Column(String(50))
"""
class AnswerAttribute:
    uid = graphene.ID()
    did = graphene.ID()
    question_id = graphene.ID()
    contents = graphene.String()

class Answer(SQLAlchemyObjectType):
    class Meta:
        model = AnswerModel
        interfaces = (relay.Node, )


class CreateAnswerInput(graphene.InputObjectType,AnswerAttribute):
    pass


class CreateAnswer(graphene.Mutation):
    answer = graphene.Field(lambda:Answer)

    class Arguments:
        input = CreateAnswerInput(required=True)
    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['created'] = datetime.utcnow()
        data['edited'] = datetime.utcnow()
        answer = AnswerModel(**data)
        db_session.add(answer)
        db_session.commit()
        #middleware 처리할
        return CreateAnswer(answer=answer)


class UpdateAnswerInput(graphene.InputObjectType, AnswerAttribute):
    """Arguments to update"""
    id = graphene.ID(required=True)


class UpdateAnswer(graphene.Mutation):
    """Update"""
    answer= graphene.Field(lambda: Answer, )

    class Arguments:
        input = UpdateAnswerInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        answer = db_session.query(AnswerModel).filter_by(id=data['id'])
        answer.update(data)
        db_session.commit()
        answer = db_session.query(AnswerModel).filter_by(id=data['id']).first()
        return UpdateAnswer(answer=answer)