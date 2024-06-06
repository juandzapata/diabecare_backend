from datetime import date

from sqlalchemy import text
from data.repositories.patient_repository import PatientRepository
from utils.constants.query import QUERY_GET_PLANES_BY_PATIENT_ID
from data.repositories.recommendation_repository import RecommendationRepository
from data.repositories.health_professional_repository import HealthProfessionalRepository
from data.models.base import PlanesPersonalizados
from schemas.personalized_planes import PersonalizedPlanCreate, PersonalizedPlanList, PersonalizedPlanOut


class PersonalizedPlanesRepository:
    def __init__(self, db):
        self.db = db
        
    def post_personalized_plan (self, plan: PersonalizedPlanCreate) -> PersonalizedPlanOut:
        professional_repository = HealthProfessionalRepository(self.db)
        profesionalPaciente = professional_repository.get_professional_patient(plan.pacienteId, plan.profesionalSaludId)
        if profesionalPaciente is None:
            return None
        
        db_plan: PlanesPersonalizados = PlanesPersonalizados(
            profesionalPacienteId = profesionalPaciente.profesionalPacienteId,
            fechaCreacion = date.today()
        )

        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
        
        self.create_recommendations_for_plan(plan, db_plan.planId)
        #notification.send_notification(plan, self.db)
        return db_plan.planId
    
    def create_recommendations_for_plan (self, plan: PersonalizedPlanCreate, planId: int) -> None:
        for i in range(len(plan.recomendaciones)):
            plan.recomendaciones[i].planId = planId
            recommendation_repository = RecommendationRepository(self.db)
            recommendation_repository.post_recomendation(plan.recomendaciones[i])
            
    def get_planes_by_user_id(self, user_id: int) -> list[PersonalizedPlanList]:
        patient_repository = PatientRepository(self.db)
        patient_id = patient_repository.get_patient_id_by_user_id(user_id)
        
        if patient_id is None:
            return None
        
        query = text(QUERY_GET_PLANES_BY_PATIENT_ID)
        result = self.db.execute(query, {"patient_id": patient_id}).fetchall()
        
        result_list: list[PersonalizedPlanList] = []
        
        for row in result:
            #Mapear
            plan = PersonalizedPlanList(
                planId=row[0],
                creation_date=row[1],
                full_name_professional=row[2]
            )
            result_list.append(plan)
        
        return result_list