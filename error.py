class myCustomError(Exception):
    def __init__(self, message, status_code):
        self.message = 'haha' +message
        self.status_code = status_code

    def __str__(self):
        return f"Error: {self.message}"