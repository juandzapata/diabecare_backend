QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID = """SELECT P.pacienteId, U.nombre, U.apellidos, U.fechaNacimiento,
       U.foto, HD.nivelGlucosa, HD.horasActividadFisica, HD.medicamento, HD.comida, HD.fecha
FROM Paciente P
INNER JOIN ProfesionalPaciente PP ON P.pacienteid = PP.pacienteId
INNER JOIN Usuario U ON P.usuarioid = U.usuarioid
INNER JOIN (
    SELECT HD1.pacienteId, HD1.nivelGlucosa, HD1.horasActividadFisica,
           HD1.medicamento, HD1.comida, HD1.fecha
    FROM HistorialDatos HD1
    INNER JOIN (
        SELECT pacienteId, MAX(fecha) AS max_fecha
        FROM HistorialDatos
        GROUP BY pacienteId
    ) HD2 ON HD1.pacienteId = HD2.pacienteId AND HD1.fecha = HD2.max_fecha
) HD ON P.pacienteid = HD.pacienteId
WHERE PP.profesionalId = :professional_id"""

QUERY_GET_USER_PATIENT_BY_ID = """
SELECT usu.usuarioId,usu.nombre,usu.apellidos, usu.correo, usu.contraseña, usu.sexo, usu.ciudad,usu.foto, usu.fechaNacimiento, usu.rolId
FROM Usuario usu
INNER JOIN Paciente pa ON pa.UsuarioId = usu.UsuarioId
WHERE pa.pacienteid = :patientId
"""
    
QUERY_GET_PATIENT_BY_ID = """SELECT P.pacienteId, CONCAT(U.nombre,' ', U.apellidos) as fullName
                                FROM Paciente P INNER JOIN Usuario U
                                ON P.usuarioId = U.usuarioId
                                WHERE P.pacienteId = :id        
                        """
QUERY_GET_PLANES_BY_PATIENT_ID = """SELECT P.planId, P.fechaCreacion, CONCAT(U.nombre, ' ', U.apellidos) as full_name_professional
                                        FROM PlanesPersonalizados P INNER JOIN ProfesionalPaciente PP
                                        on P.profesionalPacienteId = PP.profesionalPacienteId
                                        INNER JOIN ProfesionalSalud PS
                                        on PS.profesionalsaludid = PP.profesionalId
                                        INNER JOIN Usuario U
                                        on U.usuarioid = PS.usuarioid
                                        WHERE PP.pacienteId = :patient_id
                                """ 
                                
QUERY_GET_DATA_REPORT="""SELECT
    CONCAT(U.nombre, ' ', U.apellidos) AS full_name,
    U.correo,
    U.sexo,
    U.fechaNacimiento,
    FORMAT(AVG(HD.nivelGlucosa), 'N1') AS avg_nivelGlucosa,
    FORMAT(AVG(HD.horasActividadFisica), 'N1') AS avg_horasActividadFisica,
    (SELECT TOP 1 HD1.medicamento
     FROM HistorialDatos HD1
     WHERE HD1.pacienteId = P.pacienteid
     GROUP BY HD1.medicamento
     ORDER BY COUNT(HD1.medicamento) DESC) AS medicamento_mas_consumido,
    (SELECT TOP 1 HD2.comida
     FROM HistorialDatos HD2
     WHERE HD2.pacienteId = P.pacienteid
     GROUP BY HD2.comida
     ORDER BY COUNT(HD2.comida) DESC) AS comida_mas_consumida
FROM Usuario U
INNER JOIN Paciente P ON U.usuarioid = P.usuarioid
INNER JOIN HistorialDatos HD ON P.pacienteid = HD.pacienteId
WHERE P.pacienteid = :patient_id
GROUP BY U.nombre, U.apellidos, U.correo, U.sexo, U.fechaNacimiento, P.pacienteid;


"""