class Status:
    """Returned by a command to indicate success or failure."""

    def __init__(self, successful, message=""):
        """Initialize this return's success bool and message."""
        self.successful = successful
        self.message = message

    def print_message(self):
        """Print this return's message."""
        if self.message:
            print(self.message)

    def failed(self):
        """Get whether the command failed."""
        return not self.successful

