from datetime import datetime
import unittest
from pydantic import ValidationError
from requests import Session
from schemas.pdf import DataReportCreate
from exceptions.not_exists import NotExistsException
from data.database.db import SessionLocal
from schemas.patient import PatientHistoryCreate
from services.patient import PatientService


class PatientServiceTest(unittest.TestCase):
    def setUp(self):
        self.db : Session = SessionLocal()
        self.patient_service = PatientService(db=self.db)

    def test_create_history(self):

        history_create = PatientHistoryCreate(
                user_patient_id=7,
                patient_id=None,
                glucose_level=20,
                hours_physical_activity=27,
                medication="TEST",
                food="TEST"
            )

        result = self.patient_service.create_history(history_create)

        self.assertEqual(result.pacienteId, history_create.patient_id)
        self.assertEqual(result.nivelGlucosa, history_create.glucose_level)
        self.assertEqual(result.horasActividadFisica, history_create.hours_physical_activity)
        self.assertEqual(result.medicamento, history_create.medication)
        self.assertEqual(result.comida, history_create.food)
        self.assertIsNotNone(result.fecha)
        self.assertIsInstance(result.fecha, datetime)
    
    def test_create_incorrect_history(self):
        with self.assertRaises(ValidationError):
            history_create = PatientHistoryCreate(
                pacienteId=7,
                nivelGlucosa="abc",
                horasActividadFisica=27,
                medicamento="TEST",
                comida="TEST"
            )
            self.patient_service.create_history(history_create)

    def test_generate_pdf_patient_not_assigned(self):
        with self.assertRaises(NotExistsException) as context:
            data_report = DataReportCreate(patient_id=6, professional_user_id=13)
            self.patient_service.generate_pdf(data_report)
            
            self.assertEquals(context.exception.get_message(), "No existe una relación entre el paciente con id 6 y el profesional de salud con id 11")

if __name__ == '__main__':
    unittest.main()