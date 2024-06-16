from data.repositories.user_repository import UserRepository
from utils import auth, jwt as jwt
from schemas.credentials_login import CredentialsLogin
from utils.mappers.user_mapper import UserMapper

class AccountService:
    def __init__(self, db):
        self.user_repository = UserRepository(db)

    def login(self, credentials: CredentialsLogin) -> str | None:
        """
        Authenticates a user based on the provided credentials.

        Args:
            credentials (CredentialsLogin): The login credentials of the user.

        Returns:
            str | None: A JWT token if the authentication is successful, None otherwise.
        """
        user = self.user_repository.get_user_by_email(credentials.email)
        if user is None:
            return None
        if user and self.password_valid(credentials.password, user.contraseña):
            user_get = UserMapper.to_user_get_login(user)
            return jwt.create_token(user_get)
        return None

    def validate_token(self, token: str) -> dict | None:
            """
            Validates the given token and returns the decoded token data.

            Args:
                token (str): The token to be validated.

            Returns:
                dict | None: The decoded token data if the token is valid, None otherwise.
            """
            data_token = jwt.validate_token(token)
            if not data_token:
                return None
            return data_token

    def password_valid(self, password: str, password_db) -> bool:
        """
        Checks if the provided password matches the password stored in the database.

        Args:
            password (str): The password to be checked.
            password_db: The password stored in the database.

        Returns:
            bool: True if the provided password matches the password stored in the database, False otherwise.
        """
        return auth.check_password(password, password_db)
    def password_valid(self, password:str, password_db) -> bool:
        return auth.check_password(password, password_db)
