from data.models.base import TokenUsuario, Usuario


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
    
    def get_toke_user_by_user_id(self, user_id) -> TokenUsuario:
        return self.db.query(TokenUsuario).filter_by(usuarioId = user_id).first()
    
    def create_token_user(self, token: TokenUsuario) -> TokenUsuario:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token