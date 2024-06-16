from datetime import datetime
from data.models.base import HistorialDatos
from schemas.patient import PatientHistoryCreate


class PatientHistoryMapper:
    @staticmethod
    def to_patient_history_model(patient: PatientHistoryCreate) -> HistorialDatos:
        patient_model = HistorialDatos(
            pacienteId=patient.patient_id,
            nivelGlucosa=patient.glucose_level,
            horasActividadFisica=patient.hours_physical_activity,
            medicamento=patient.medication,
            comida=patient.food,
            fecha = datetime.today()
        )
        return patient_model