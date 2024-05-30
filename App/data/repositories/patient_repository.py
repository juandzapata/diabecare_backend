from data.models.base import HistorialDatos


class PatientRepository:
    def __init__(self, db):
        self.db = db

    def create(self, history: HistorialDatos) -> HistorialDatos:
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_history_by_patient_id(self, patient_id: int):
        return self.db.query(HistorialDatos).filter(HistorialDatos.pacienteId == patient_id).all()