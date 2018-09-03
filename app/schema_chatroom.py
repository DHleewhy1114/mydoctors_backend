import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Chatroom as ChatroomModel, Base
from utils import input_to_dictionary
from datetime import datetime
import schema_messagerecipient
from flask_jwt_extended import current_user, jwt_required
"""
  class Chatroom(Base):
    __tablename__='chatroom'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    created = Column(String(50))
    edited = Column(String(50))
"""
class ChatroomAttribute:
    uid = graphene.ID()
    did = graphene.ID()

class Chatroom(SQLAlchemyObjectType):
    class Meta:
        model = ChatroomModel
        interfaces = (relay.Node, )


class CreateChatroomInput(graphene.InputObjectType, ChatroomAttribute):
    pass


class CreateChatroom(graphene.Mutation):
    chatroom= graphene.Field(lambda:Chatroom)

    class Arguments:
        input = CreateChatroomInput(required=True)
    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['created'] = datetime.utcnow()
        data['edited'] = datetime.utcnow()
        chatroom = ChatroomModel(**data)
        db_session.add(chatroom)
        db_session.commit()
        #middleware 처리할
        return CreateChatroom(chatroom = chatroom)

"""
class UpdateChatroomInput(graphene.InputObjectType, ChatroomAttribute):
    #Arguments to update
    id = graphene.ID(required=True)


class UpdateChatroom(graphene.Mutation):
    #Update
    chatroom = graphene.Field(lambda: Chatroom, )

    class Arguments:
        input = UpdateChatroomInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        chatroom = db_session.query(MessageModel).filter_by(id=data['id'])
        chatroom.update(data)
        db_session.commit()
        chatroom = db_session.query(ChatroomModel).filter_by(id=data['id']).first()

        return UpdateChatroom(chatroom=chatroom)
    """