class TaskException(Exception):
    """Base class for exceptions in this module."""
    pass
  
class FailedToGetTaskException(TaskException):
    """Exception raised when a task is not found."""
    def __init__(self, task_id):
        self.task_id = task_id
        self.message = f"Task with id {task_id} not found."
        super().__init__(self.message)
        
class FailedToCreateTaskException(TaskException):
    """Exception raised when a task creation fails."""
    def __init__(self, reason):
        self.reason = reason
        self.message = f"Failed to create task: {reason}"
        super().__init__(self.message)
        
class FailedToUpdateTaskException(TaskException):
    """Exception raised when a task update fails."""
    def __init__(self, task_id, reason):
        self.task_id = task_id
        self.reason = reason
        self.message = f"Failed to update task with id {task_id}: {reason}"
        super().__init__(self.message)

class FailedToDeleteTaskException(TaskException):
    """Exception raised when a task deletion fails."""
    def __init__(self, task_id, reason):
        self.task_id = task_id
        self.reason = reason
        self.message = f"Failed to delete task with id {task_id}: {reason}"
        super().__init__(self.message)
        
class InvalidTaskStatusException(TaskException):
    """Exception raised when an invalid task status is provided."""
    def __init__(self, status):
        self.status = status
        self.message = f"Invalid task status: {status}. Valid statuses are 'pending', 'in_progress', 'completed'."
        super().__init__(self.message)  
        
class AuthException(Exception):
    """Base class for authentication exceptions."""
    pass

class AuthenticationFailedException(AuthException):
    """Exception raised when authentication fails."""
    def __init__(self, reason):
        self.reason = reason
        self.message = f"Authentication failed: {reason}"
        super().__init__(self.message)
        
class UserAlreadyExistsException(AuthException):
    """Exception raised when trying to register a user that already exists."""
    def __init__(self, email):
        self.email = email
        self.message = f"User with email {email} already exists."
        super().__init__(self.message)
        
class UserNotFoundException(AuthException):
    """Exception raised when a user is not found."""
    def __init__(self, email):
        self.email = email
        self.message = f"User with email {email} not found."
        super().__init__(self.message)
        
class InvalidCredentialsException(AuthException):
    """Exception raised when provided credentials are invalid."""
    def __init__(self):
        self.message = "Invalid email or password."
        super().__init__(self.message)
        
class TokenGenerationException(AuthException):
    """Exception raised when token generation fails."""
    def __init__(self, reason):
        self.reason = reason
        self.message = f"Failed to generate token: {reason}"
        super().__init__(self.message)
        
class TokenValidationException(AuthException):
    """Exception raised when token validation fails."""
    def __init__(self, reason):
        self.reason = reason
        self.message = f"Token validation failed: {reason}"
        super().__init__(self.message)
        
class AuthorizationException(AuthException):
    """Exception raised when authorization fails."""
    def __init__(self, reason):
        self.reason = reason
        self.message = f"Authorization failed: {reason}"
        super().__init__(self.message)
        