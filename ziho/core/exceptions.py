class BaseZihoError(Exception):
    """
    Root exception for Ziho.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class PersistenceError(BaseZihoError):
    """
    Used to catch down errors when persisting models to the database instead
    of letting all issues percolate up.
    """
