"""
core/exceptions.py — Application-specific exceptions.

These decouple the service/repository layers from HTTP concerns.
Repositories raise these when business/DB rules are violated, and the
FastAPI exception handlers in main.py translate them to 404/422 responses.
"""

class NotFoundError(Exception):
    """Raised by repositories when a requested entity (by ID) does not exist."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ValidationError(Exception):
    """Raised by services when business rules or validations fail."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
