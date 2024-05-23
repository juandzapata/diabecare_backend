"""
class PlanesPersonalizados(Base):
    __tablename__ = 'PlanesPersonalizados'
    planId = Column(Integer, primary_key=True, autoincrement=True)
    pacienteId = Column(Integer, ForeignKey('Paciente.pacienteId'))
    profesionalSaludId = Column(Integer, ForeignKey('ProfesionalSalud.profesionalSaludId'))
    fechaCreacion = Column(Date)
    paciente = relationship("Paciente")
    profesionalSalud = relationship("ProfesionalSalud")
"""
from pydantic import BaseModel
from sqlalchemy import Date

class PlanPersonalizadoCreate (BaseModel):
    pacienteId = int
    profesionalSaludId = int
    fechaCreacion = Date
    recomendaciones = list

class PlanesPersonalizadosOut (BaseModel):
    planId: int