from datetime import date
from schemas.patient import PatientList

class PatientListMapper:
    
    @staticmethod
    def to_patient_list_model(patient) -> PatientList:
        actual_year = date.today().year
        age = actual_year - patient.fechaNacimiento.year
        return PatientList(
                patient_id=patient.pacienteId,
                name=patient.nombre,
                last_name=patient.apellidos,
                photo=patient.foto,
                age = age,
                glucose_level=patient.nivelGlucosa,
                physical_activity_hours=patient.horasActividadFisica,
                last_medication=patient.medicamento,
                last_meal=patient.comida,
                date=patient.fecha)
        