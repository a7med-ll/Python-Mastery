from logger import LoggerManager

class UserService:

    def __init__(self):
        self.logger = LoggerManager.get_logger(__name__)

    def create_user(self, username):
        self.logger.info(f"Creating user {username}")

        if not isinstance(username, str) or not username.strip():

            self.logger.error("Invalid username")
            raise ValueError("Invalid username")

        username = username.strip()

        self.logger.info("User created successfully")
        return f"{username} created successfully"
