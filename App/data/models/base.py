from sqlalchemy import DECIMAL, Column, Date, DateTime, ForeignKey, Integer, String, Time
from data.database.db import Base
from sqlalchemy.orm import relationship
    
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
    rolId = Column(Integer, ForeignKey('Rol.rolId'))

    
class Rol(Base):
    __tablename__ = 'Rol'
    rolId = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    
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
    profesionalPacienteId = Column(Integer, ForeignKey('ProfesionalPaciente.profesionalPacienteId'))
    fechaCreacion = Column(Date)

    
class Recomendacion(Base):
    __tablename__ = 'Recomendacion'
    recomendacionId = Column(Integer, primary_key=True, autoincrement=True)
    planId = Column(Integer, ForeignKey('PlanesPersonalizados.planId'))
    estado = Column(String(50))
    actividad = Column(String(255))
    horaEjecucion = Column(Time(0))
    titulo = Column(String(100))
    plan = relationship("PlanesPersonalizados")

class HistorialDatos(Base):
    __tablename__ = 'HistorialDatos'
    historialDatosId = Column(Integer, primary_key=True, autoincrement=True)
    nivelGlucosa = Column(DECIMAL(10,2))
    horasActividadFisica = Column(DECIMAL(10, 2))
    medicamento = Column(String(100))
    comida = Column(String(255))
    fecha = Column(DateTime)
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
    
class ProfesionalPaciente(Base):
    __tablename__ = 'ProfesionalPaciente'
    profesionalPacienteId = Column(Integer, primary_key=True, autoincrement=True)
    profesionalId = Column(Integer, ForeignKey('ProfesionalSalud.profesionalSaludId')) 
    pacienteId = Column(Integer, ForeignKey('Paciente.pacienteId'))
    
class TokenUsuario(Base):
    __tablename__ = 'TokenUsuario'
    tokenUsuarioId = Column(Integer, primary_key=True, autoincrement=True)
    usuarioId = Column(Integer, ForeignKey('Usuario.usuarioId'))
    tokenDispositivo = Column(String(255))