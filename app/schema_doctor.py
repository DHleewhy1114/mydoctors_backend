import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Doctor as DoctorModel, Base
from utils import input_to_dictionary
from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
"""
__tablename__='doctor'
    id = Column(Integer, primary_key=True)
    doctorname = Column(String(64), index=True)
    hospital_id = Column(Integer,ForeignKey('hospital.id'),nullable=False)
"""
class DoctorAttribute:
    doctor_name = graphene.String()
    hospital_id = graphene.ID()
    doctor_code = graphene.Int()


class Doctor(SQLAlchemyObjectType):
    class Meta:
        model = DoctorModel
        interfaces = (relay.Node, )

class CreateDoctorInput(graphene.InputObjectType, DoctorAttribute):
    pass

class CreateDoctor(graphene.Mutation):
    doctor = graphene.Field(lambda:Doctor)

    class Arguments:
        input = CreateDoctorInput(required=True)
    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['created'] = datetime.utcnow()
        data['edited'] = datetime.utcnow()
        doctor = DoctorModel(**data)
        db_session.add(doctor)
        db_session.commit()
        return CreateDoctor(doctor=doctor)


class UpdateDoctorInput(graphene.InputObjectType, DoctorAttribute):
    """Arguments to update"""
    id = graphene.ID(required=True)


class UpdateDoctor(graphene.Mutation):
    """Update"""
    doctor = graphene.Field(lambda: Doctor, )

    class Arguments:
        input = UpdateDoctorInput(required=True)

    def mutate(self, info, input):
        data = input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        doctor = db_session.query(DoctorModel).filter_by(id=data['id'])
        doctor.update(data)
        db_session.commit()
        doctor = db_session.query(DoctorModel).filter_by(id=data['id']).first()

        return UpdateDoctor(doctor=doctor)
