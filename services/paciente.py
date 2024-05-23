from datetime import date

from sqlalchemy import text
from schemas.paciente import PacienteLista
def obtener_info_pacientes_por_profesional(db, profesional_id: int) -> list[PacienteLista]:
    print(profesional_id)
    query = text(""" 
    SELECT P.pacienteId, CONCAT(U.nombre, ' ', U.apellidos) as nombre_completo, U.fechaNacimiento,
            U.foto, HD.nivelGlucosa, HD.horasActividadFisica, HD.medicamento, HD.comida, HD.fecha
    FROM Paciente P INNER JOIN ProfesionalPaciente PP
    ON P.pacienteid = PP.pacienteId INNER JOIN HistorialDatos HD
    ON P.pacienteid = HD.pacienteId INNER JOIN Usuario U
    ON P.usuarioid = U.usuarioid
    WHERE PP.profesionalId = :profesional_id
    """)
    result = db.execute(query, {"profesional_id": profesional_id}).fetchall()
    
    result_list = []
    
    for row in result:
        ano_actual = date.today().year
        edad = ano_actual - row.fechaNacimiento.year
        paciente = PacienteLista(
            paciente_id=row.pacienteId,
            nombre_completo=row.nombre_completo,
            edad = edad,
            foto=row.foto,
            nivel_glucosa=row.nivelGlucosa,
            actividad_fisica=row.horasActividadFisica,
            medicamento=row.medicamento,
            ultima_comida=row.comida,
            fecha_actualizacion=row.fecha
        )
        result_list.append(paciente)
    
    return result_list