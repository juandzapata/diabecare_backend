QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID = """SELECT P.pacienteId, U.nombre, U.apellidos, U.fechaNacimiento,
            U.foto, HD.nivelGlucosa, HD.horasActividadFisica, HD.medicamento, HD.comida, HD.fecha
    FROM Paciente P INNER JOIN ProfesionalPaciente PP
    ON P.pacienteid = PP.pacienteId INNER JOIN HistorialDatos HD
    ON P.pacienteid = HD.pacienteId INNER JOIN Usuario U
    ON P.usuarioid = U.usuarioid
    WHERE PP.profesionalId = :profesional_id"""

QUERY_GET_USER_PATIENT_BY_ID = """
SELECT usu.usuarioid,usu.nombre,usu.apellidos, usu.correo, usu.contraseña, usu.sexo, usu.foto, usu.fechaNacimiento, usu.rolId
FROM Usuario usu
INNER JOIN Paciente pa ON pa.UsuarioId = usu.UsuarioId
WHERE pa.pacienteid = :patientId
"""
    
QUERY_GET_PATIENT_BY_ID = """SELECT P.pacienteId, CONCAT(U.nombre,' ', U.apellidos) as fullName
                                FROM Paciente P INNER JOIN Usuario U
                                ON P.usuarioId = U.usuarioId
                                WHERE P.pacienteId = :id        
                        """
QUERY_GET_PLANES_BY_PATIENT_ID = """SELECT P.planid, P.fechacreacion, CONCAT(U.nombre, ' ', U.apellidos) as full_name_professional
                                        FROM PlanesPersonalizados P INNER JOIN ProfesionalPaciente PP
                                        on P.profesionalPacienteId = PP.profesionalPacienteId
                                        INNER JOIN ProfesionalSalud PS
                                        on PS.profesionalsaludid = PP.profesionalId
                                        INNER JOIN Usuario U
                                        on U.usuarioid = PS.usuarioid
                                        WHERE PP.pacienteId = :patient_id
                                """ 