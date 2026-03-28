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