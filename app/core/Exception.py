class AppBaseException(Exception):
    status_code: int
    
    def __init__(self, message: str | None = None):
        self.message = message or "An error occurred"
        super().__init__(self.message)

class ApplicationException(AppBaseException):
    status_code = 400
    
    def __init__(self, message: str | None = None):
        super().__init__(message or "Application error occurred")

class RepositoryException(AppBaseException):
    status_code = 500
    
    def __init__(self, message: str | None = None):
        super().__init__(message or "Database error occurred")

class SSHConnectionException(AppBaseException):
    status_code = 503
    
    def __init__(self, message: str | None = None):
        super().__init__(message or "SSH connection failed")

class SecurityException(AppBaseException):
    status_code = 401
    
    def __init__(self, message: str | None = None):
        super().__init__(message or "Security exception occurred")

class ServerNotFoundException(AppBaseException):
    status_code = 404
    
    def __init__(self, message: str | None = None):
        super().__init__(message or "Server not found")

class AuthorizationException(AppBaseException):
    status_code = 403
    
    def __init__(self, message: str | None = None):
        super().__init__(message or "Unauthorized. superadmin access required")