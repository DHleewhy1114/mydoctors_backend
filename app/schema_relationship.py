import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Relationship as RelationshipModel, Base
from utils import input_to_dictionary
from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
import base64
"""
   class relationship(Base):
    __tablename__='relationship'
    id = Column(Integer,primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    did = Column(Integer, ForeignKey('doctor.id'), nullable=False)
"""
class RelationshipAttribute:
    uid = graphene.ID()
    did = graphene.ID()

class Relationship(SQLAlchemyObjectType):
    class Meta:
        model = RelationshipModel
        interfaces = (relay.Node, )

class CreateRelationshipInput(graphene.InputObjectType, RelationshipAttribute):
    pass

class CreateRelationship(graphene.Mutation):
    relationship = graphene.Field(lambda:Relationship)

    class Arguments:
        input = CreateRelationshipInput(required=True)
    def mutate(self, info, input):
        isExist=False
        uid= base64.b64decode(input.uid)
        did= base64.b64decode(input.did)
        int_uid = int(str(uid)[7:-1])
        int_did = int(str(did)[9:-1])
        query_by_uid = db_session.query(RelationshipModel).filter_by(uid=int_uid,did=int_did)
        if(query_by_uid.all()!=[]):
            print ("isexist")
            return
        else:
            data = input_to_dictionary(input)
            data['created'] = datetime.utcnow()
            data['edited'] = datetime.utcnow()
            relationship = RelationshipModel(**data)
            db_session.add(relationship)
            db_session.commit()
            return CreateRelationship(relationship=relationship)
        

class UpdateRelationshipInput(graphene.InputObjectType, RelationshipAttribute):
    """Arguments to update"""
    id = graphene.ID(required=True)


class UpdateRelationship(graphene.Mutation):
    """Update"""
    relationship = graphene.Field(lambda: Relationship, )

    class Arguments:
        input = UpdateRelationshipInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        relationship = db_session.query(RelationshipModel).filter_by(id=data['id'])
        relationship.update(data)
        db_session.commit()
        relationship = db_session.query(RelationshipModel).filter_by(id=data['id']).first()

        return UpdateRelationship(relationship=relationship)
