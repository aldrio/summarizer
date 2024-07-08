
class PublicError(Exception):
    def __init__(self, message, original_exception=None):
        self.message = message
        self.original_exception = original_exception
