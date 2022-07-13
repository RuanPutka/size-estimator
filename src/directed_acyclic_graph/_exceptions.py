class CycleError(Exception):
    """Top-level error for validating numbers.
    This exception should normally not be raised, only subclasses of this
    exception."""

    def __init__(self):
        self.message = "Cycle was formed."

    def __str__(self):
        """Return the exception message."""
        return self.message
