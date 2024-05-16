from decimal import Decimal
from sqlalchemy import DECIMAL, Column, Date, DateTime, ForeignKey, Integer, String
from database.db import Base
from sqlalchemy.orm import relationship
class UsuarioRol(Base):
    __tablename__ = 'UsuarioRol'
    usuarioId = Column(Integer, ForeignKey('Usuario.usuarioId'), primary_key=True)
    rolId = Column(Integer, ForeignKey('Rol.rolId'), primary_key=True)
    
class Usuario(Base):
    __tablename__ = 'Usuario'
    usuarioId = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    apellidos = Column(String(100))
    correo = Column(String, unique=True)
    contraseña = Column(String(100))
    sexo = Column(String(1))
    ciudad = Column(String(100))
    foto = Column(String(255), nullable=True)
    fechaNacimiento = Column(Date)
    roles = relationship("Rol", secondary="UsuarioRol")
    
class Rol(Base):
    __tablename__ = 'Rol'
    rolId = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    usuarios = relationship("Usuario", secondary="UsuarioRol")
    
class Paciente(Base):
    __tablename__ = 'Paciente'
    pacienteId = Column(Integer, primary_key=True, autoincrement=True)
    usuarioId = Column(Integer, ForeignKey('Usuario.usuarioId'))
    historiaClinica = Column(String(255), nullable=True)
    planTratamiento = Column(String(255), nullable=True)
    usuario = relationship("Usuario")
    
class ProfesionalSalud(Base):
    __tablename__ = 'ProfesionalSalud'
    profesionalSaludId = Column(Integer, primary_key=True, autoincrement=True)
    usuarioId = Column(Integer, ForeignKey('Usuario.usuarioId'))
    tarjetaProfesional = Column(String(255), nullable=True)
    centroMedico = Column(String(255), nullable=True)
    especialidad = Column(String(100), nullable=True)
    usuario = relationship("Usuario")
    
    
class ContenidoEducativo(Base):
    __tablename__ = 'ContenidoEducativo'
    contenidoId = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100))
    cuerpo = Column(String(max))
    
class Recurso(Base):
    __tablename__ = 'Recurso'
    recursoId = Column(Integer, primary_key=True, autoincrement=True)
    contenidoId = Column(Integer, ForeignKey('ContenidoEducativo.contenidoId'))
    tipo = Column(String(50))
    url = Column(String(255))
    
class PlanesPersonalizados(Base):
    __tablename__ = 'PlanesPersonalizados'
    planId = Column(Integer, primary_key=True, autoincrement=True)
    pacienteId = Column(Integer, ForeignKey('Paciente.pacienteId'))
    profesionalSaludId = Column(Integer, ForeignKey('ProfesionalSalud.profesionalSaludId'))
    fechaCreacion = Column(Date)
    paciente = relationship("Paciente")
    profesionalSalud = relationship("ProfesionalSalud")
    
class Recomendacion(Base):
    __tablename__ = 'Recomendacion'
    recomendacionId = Column(Integer, primary_key=True, autoincrement=True)
    planId = Column(Integer, ForeignKey('PlanesPersonalizados.planId'))
    estado = Column(String(50))
    actividad = Column(String(255))
    fechaEjecucion = Column(DateTime)
    plan = relationship("PlanesPersonalizados")

class HistorialDatos(Base):
    __tablename__ = 'HistorialDatos'
    historialDatosId = Column(Integer, primary_key=True, autoincrement=True)
    nivelGlucosa = Column(DECIMAL(10,2))
    horasActividadFisica = Column(DECIMAL(10, 2))
    medicamento = Column(String(100))
    comida = Column(String(255))
    fecha = Column(Date)
    pacienteId = Column(Integer, ForeignKey('Paciente.pacienteId'))
    paciente = relationship("Paciente")

class Favorito(Base):
    __tablename__ = 'Favorito'
    favoritoId = Column(Integer, primary_key=True, autoincrement=True)
    pacienteId = Column(Integer, ForeignKey('Paciente.pacienteId'))
    contenidoId = Column(Integer, ForeignKey('ContenidoEducativo.contenidoId'))
    fecha = Column(Date)
    paciente = relationship("Paciente") 
    contenido = relationship("ContenidoEducativo")
    
class Notificacion(Base):
    __tablename__ = 'Notificacion'
    notificacionId = Column(Integer, primary_key=True, autoincrement=True)
    pacienteId = Column(Integer, ForeignKey('Paciente.pacienteId'))
    fechaRepeticion = Column(DateTime)
    mensaje = Column(String(max))