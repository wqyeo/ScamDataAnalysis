class TaskThread:
    def __init__(self, name:str, description="", isRunning=True) -> None:
        """
        An object used to keep track of Function state in Threads
        """
        self.name = name
        self.description = description
        self.isRunning = isRunning
        pass