import logging

class MyLogger(logging.Logger):
    def __init__(self, name, level=logging.DEBUG):
        super(MyLogger, self).__init__(name, level)

        # Create a console handler and set the level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create a formatter and attach it to the handler
        formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.addHandler(console_handler)

# Example usage
if __name__ == "__main__":
    logger = MyLogger(__name__)

    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")

