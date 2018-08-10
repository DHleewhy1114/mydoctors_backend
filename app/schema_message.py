import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Message as MessageModel, Messagerecipient as MessagerecipientModel, Base
from utils import input_to_dictionary
from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
"""
  class Message(Base):
    __tablename__='message'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    parent_id = Column(Integer,ForeignKey('question.id'),nullable=True)
    content = Column(String(1000))
"""
class MessageAttribute:
    uid = graphene.ID()
    did = graphene.ID()
    parent_id = graphene.ID()
    content = graphene.String()

class Message(SQLAlchemyObjectType):
    class Meta:
        model = MessageModel
        interfaces = (relay.Node, )

class CreateMessageInput(graphene.InputObjectType, MessageAttribute):
    pass

class CreateMessage(graphene.Mutation):
    message = graphene.Field(lambda:Message)

    class Arguments:
        input = CreateMessageInput(required=True)
    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['created'] = datetime.utcnow()
        data['edited'] = datetime.utcnow()
        message = MessageModel(**data)
        db_session.add(message)
        db_session.commit()
        return CreateMessage(message=message)


class UpdateMessageInput(graphene.InputObjectType, MessageAttribute):
    """Arguments to update"""
    id = graphene.ID(required=True)


class UpdateMessage(graphene.Mutation):
    """Update"""
    message = graphene.Field(lambda: Message, )

    class Arguments:
        input = UpdateMessageInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        message = db_session.query(MessageModel).filter_by(id=data['id'])
        message.update(data)
        db_session.commit()
        message = db_session.query(MessageModel).filter_by(id=data['id']).first()

        return UpdateMessage(message=message)
