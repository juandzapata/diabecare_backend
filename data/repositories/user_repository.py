from data.models.base import Usuario


class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_user_by_email(self, email: str, db) -> Usuario:
        user = db.query(Usuario).filter(Usuario.correo == email).first()
        return user
    
    def get_all_users(self, db) -> list[Usuario]:
        users = db.query(Usuario).all()
        return users
    
    def get_user_by_id(self, user_id: int, db) -> Usuario:
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        return user
    
    def create_user(self, user: Usuario, db) -> Usuario:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    