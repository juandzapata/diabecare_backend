from datetime import datetime
import unittest

from requests import Session

from data.database.db import SessionLocal
from schemas.patient import PatientHistoryCreate
from services.patient import PatientService


class PatientServiceTest(unittest.TestCase):
    def setUp(self):
        self.db : Session = SessionLocal()
        self.patient_service = PatientService(db=self.db)

    def test_create_history(self):

        history_create = PatientHistoryCreate(
                pacienteId=7,
                nivelGlucosa=20,
                horasActividadFisica=27,
                medicamento="TEST",
                comida="TEST"
            )

        result = self.patient_service.create_history(history_create)

        self.assertEqual(result.pacienteId, history_create.pacienteId)
        self.assertEqual(result.nivelGlucosa, history_create.nivelGlucosa)
        self.assertEqual(result.horasActividadFisica, history_create.horasActividadFisica)
        self.assertEqual(result.medicamento, history_create.medicamento)
        self.assertEqual(result.comida, history_create.comida)
        self.assertIsNotNone(result.fecha)
        self.assertIsInstance(result.fecha, datetime)

if __name__ == '__main__':
    unittest.main()