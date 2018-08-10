import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, User as UserModel, Base
from utils import input_to_dictionary
from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
"""
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password_hash = Column(String(256))
    created = Column(String(50))
    edited = Column(String(50))
"""
class UserAttribute:
    username = graphene.String()
    password_hash = graphene.String()

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )

class CreateUserInput(graphene.InputObjectType, UserAttribute):
    pass

class CreateUser(graphene.Mutation):
    user = graphene.Field(lambda:User)

    class Arguments:
        input = CreateUserInput(required=True)
    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['created'] = datetime.utcnow()
        data['edited'] = datetime.utcnow()
        #data['password_hash']=UserModel.set_password(data['password_hash'])
        user = UserModel(**data)
        db_session.add(user)
        db_session.commit()
        return CreateUser(user=user)


class UpdateUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to update"""
    id = graphene.ID(required=True)


class UpdateUser(graphene.Mutation):
    """Update"""
    user = graphene.Field(lambda: User, )

    class Arguments:
        input = UpdateUserInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        user = db_session.query(UserModel).filter_by(id=data['id'])
        user.update(data)
        db_session.commit()
        user = db_session.query(UserModel).filter_by(id=data['id']).first()

        return UpdateUser(user=user)
