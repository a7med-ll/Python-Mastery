from config import ConfigManager
from payment import PaymentService
from user import UserService


def main():
    try:
        config = ConfigManager()
        config.load("config.json")

        app_name = config.get_config("app_name")
        print(f"Application: {app_name}")

        username = input("Enter username: ").strip()

        amount_input = input("Enter payment amount: ").strip()
        amount = float(amount_input)

        user_service = UserService()
        payment_service = PaymentService()

        user_result = user_service.create_user(username)
        payment_result = payment_service.process_payment(amount)

        print(user_result)
        print(payment_result)

    except FileNotFoundError as error:
        print(f"Configuration file error: {error}")

    except ValueError as error:
        print(f"Validation error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()