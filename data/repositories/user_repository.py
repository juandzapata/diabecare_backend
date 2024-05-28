from data.models.base import Usuario


class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_user_by_email(self, email: str, db) -> Usuario:
        user = db.query(Usuario).filter(Usuario.correo == email).first()
        return user