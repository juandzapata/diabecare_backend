from datetime import date
from sqlalchemy import text
from utils.mappers.plan_list_mapper import PersonalizedPlanMapper
from utils.constants.query import QUERY_GET_PLANES_BY_PATIENT_ID
from data.models.base import PlanesPersonalizados
from schemas.personalized_planes import PersonalizedPlanList


class PersonalizedPlanesRepository:
    """
    Repository class for managing personalized plans.
    """

    def __init__(self, db):
        self.db = db
  
    def post_personalized_plan (self, professional_patient_id: int) -> PlanesPersonalizados:
        db_plan: PlanesPersonalizados = PlanesPersonalizados(
            profesionalPacienteId = professional_patient_id,
            fechaCreacion = date.today()
        )

        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
       
        return db_plan
            
    def get_planes_by_patient_id(self, patient_id: int) -> list[PersonalizedPlanList]:   
        query = text(QUERY_GET_PLANES_BY_PATIENT_ID)
        planes = self.db.execute(query, {"patient_id": patient_id}).fetchall()
        planes_list: list[PersonalizedPlanList] = []
        for plan in planes:
            plan = PersonalizedPlanMapper.to_plan_list_model(plan)
            planes_list.append(plan)
        return planes_list