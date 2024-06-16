from data.models.base import Usuario
from data.repositories.user_repository import UserRepository
from schemas.user import UserRead

class UserService:
    def __init__(self, db):
        self.user_repository = UserRepository(db)
        
    def all_users(self) -> list[UserRead]:
            """
            Retrieves all users from the user repository.

            Returns:
                A list of UserRead objects representing all the users.
            """
            users = self.user_repository.get_all_users()
            return [UserRead.from_orm(user) for user in users]
