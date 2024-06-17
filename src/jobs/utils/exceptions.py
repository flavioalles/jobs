class InvalidTransitionError(Exception):
    """
    (Base) Exception raised when an invalid transition is attempted.
    To be used as a base class for more specific exceptions (e.g. Job and Application-related).

    Attributes:
        old (str): The old state of the transition.
        new (str): The new state of the transition.
    """

    def __init__(self, old: str, new: str) -> None:
        super().__init__(f"Invalid transition: {old} to {new}.")
