
class UserModel:
    @staticmethod
    def get_by_cognito_username(cognito_username: str) -> dict:
        # sql query to fetch user from database by cognito username
        pass

    @staticmethod
    def update_by_id(id: int, update_body: dict) -> dict:
        # sql query to update user by id
        pass
