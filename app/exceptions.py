class EnvironmentValueNotFound(Exception):
    def __init__(self, value="value"):
        self.value = value

    def __repr__(self):
        return f"environment variable \"{self.value}\" is not found."
