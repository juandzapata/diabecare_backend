from schemas.personalized_planes import PersonalizedPlanList


class PersonalizedPlanMapper:
    
    @staticmethod
    def to_plan_list_model(plan) -> PersonalizedPlanList:
        return PersonalizedPlanList(
            planId=plan.planId,
            creation_date=plan.fechaCreacion,
            full_name_professional=plan.full_name_professional
        )