from datetime import date
from schemas.patient import PatientDataReport


class PatientDataReportMapper:
    
    @staticmethod
    def to_patient_data_report_model(patient) -> PatientDataReport:
        age = date.today().year - patient.fechaNacimiento.year
        return PatientDataReport(
            full_name=patient.full_name,
            email=patient.correo,
            gender=patient.sexo,
            age=age,
            average_glucose_level=patient.avg_nivelGlucosa,
            average_physical_activity_hours=patient.avg_horasActividadFisica,
            most_consumed_medication=patient.medicamento_mas_consumido,
            most_consumed_food=patient.comida_mas_consumida,
            full_name_professional=None,
            email_professional=None
        )
    