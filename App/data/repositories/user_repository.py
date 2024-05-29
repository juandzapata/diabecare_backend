from data.models.base import Usuario


class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_user_by_email(self, email: str) -> Usuario:
        user = self.db.query(Usuario).filter(Usuario.correo == email).first()
        return user
    
    def get_all_users(self) -> list[Usuario]:
        users = self.db.query(Usuario).all()
        return users
    
    def get_user_by_id(self, user_id: int) -> Usuario:
        user = self.db.query(Usuario).filter(Usuario.id == user_id).first()
        return user
    
    def create_user(self, user: Usuario) -> Usuario:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    