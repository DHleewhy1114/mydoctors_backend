import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Hospital as HospitalModel, Base
from utils import input_to_dictionary
from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
"""
   class Hospital(Base):
    __tablename__='hospital'
    id = Column(Integer, primary_key=True)
    Hospitalname = Column(String(1000))
    position_x = Column(Integer)
    position_y = Column(Integer)
"""
class HospitalAttribute:
    hospital_name = graphene.String()
    position_x = graphene.Int()
    position_y = graphene.Int()

class Hospital(SQLAlchemyObjectType):
    class Meta:
        model = HospitalModel
        interfaces = (relay.Node, )

class CreateHospitalInput(graphene.InputObjectType, HospitalAttribute):
    pass

class CreateHospital(graphene.Mutation):
    hospital = graphene.Field(lambda:Hospital)

    class Arguments:
        input = CreateHospitalInput(required=True)
    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['created'] = datetime.utcnow()
        data['edited'] = datetime.utcnow()
        hospital = HospitalModel(**data)
        db_session.add(hospital)
        db_session.commit()
        return CreateHospital(hospital=hospital)


class UpdateHospitalInput(graphene.InputObjectType, HospitalAttribute):
    """Arguments to update"""
    id = graphene.ID(required=True)


class UpdateHospital(graphene.Mutation):
    """Update"""
    Hospital = graphene.Field(lambda: Hospital, )

    class Arguments:
        input = UpdateHospitalInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        hospital = db_session.query(HospitalModel).filter_by(id=data['id'])
        hospital.update(data)
        db_session.commit()
        hospital = db_session.query(HospitalModel).filter_by(id=data['id']).first()

        return UpdateHospital(hospital=hospital)
