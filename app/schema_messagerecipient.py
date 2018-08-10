import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Messagerecipient as MessagerecipientModel, Base
from utils import input_to_dictionary
from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
"""
   class Messagerecipient(Base):
    __tablename__='messagerecipient'
    id = Column(Integer, primary_key=True)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    message_id = Column(Integer, ForeignKey('message.id'), nullable=False)

"""
class MessagerecipientAttribute:
    recipient_id = graphene.ID()
    message_id = graphene.ID()

class Messagerecipient(SQLAlchemyObjectType):
    class Meta:
        model = MessagerecipientModel
        interfaces = (relay.Node, )

class CreateMessagerecipientInput(graphene.InputObjectType, MessagerecipientAttribute):
    pass

class CreateMessagerecipient(graphene.Mutation):
    messagerecipient = graphene.Field(lambda:Messagerecipient)

    class Arguments:
        input = CreateMessagerecipientInput(required=True)
    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['created'] = datetime.utcnow()
        data['edited'] = datetime.utcnow()
        messagerecipient = MessagerecipientModel(**data)
        db_session.add(messagerecipient)
        db_session.commit()
        return CreateMessagerecipient(messagerecipient=messagerecipient)


class UpdateMessagerecipientInput(graphene.InputObjectType, MessagerecipientAttribute):
    """Arguments to update"""
    id = graphene.ID(required=True)


class UpdateMessage(graphene.Mutation):
    """Update"""
    messagerecipient = graphene.Field(lambda: Messagerecipient, )

    class Arguments:
        input = UpdateMessagerecipientInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        messagerecipient = db_session.query(MessagerecipientModel).filter_by(id=data['id'])
        messagerecipient.update(data)
        db_session.commit()
        messagerecipient = db_session.query(MessagerecipientModel).filter_by(id=data['id']).first()

        return UpdateMessagerecipient(messagerecipient=messagerecipient)
