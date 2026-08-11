class RAGException(Exception):
    """Base exception for RAG platform"""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationException(RAGException):
    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")


class DatabaseException(RAGException):
    def __init__(self, message: str):
        super().__init__(message, code="DATABASE_ERROR")
