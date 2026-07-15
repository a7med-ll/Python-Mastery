from logger import LoggerManager

class PaymentService:

    def __init__(self):
        self.logger = LoggerManager.get_logger(__name__)

    def process_payment(self,amount):

        self.logger.info(f"Processing Payment of {amount}")

        if amount <= 0:
            self.logger.error("Payment amount must be greater than zero")
            raise ValueError("Payment amount must be greater than zero")


        self.logger.info("Payment completed successful")
        return f"Payment of {amount} completed successfully"

