from data.models.base import TokenUsuario


class TokenUserRepository:
    def __init__(self, db):
        self.db = db

    def create(self, token_user):
        self.db.session.add(token_user)
        self.db.session.commit()

    def get_by_token(self, token):
        return self.db.session.query(TokenUsuario).filter_by(token=token).first()

    def get_by_user_id(self, user_id):
        return self.db.query(TokenUsuario).filter_by(usuarioId = user_id).first()

    def delete(self, token_user):
        self.db.session.delete(token_user)
        self.db.session.commit()