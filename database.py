class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    def __init__(self):
        # Parse and connect to database

        # Handle connection errors gracefully
    def tryPrint(self):
        print("HI")

logger = Logger()
logger.tryPrint()
