class GameError(Exception):
    """Base class for other exceptions"""
    pass


class WrongShipsPosition(Exception):
    """Raised when cannot fill the field with ships according the rules
    Attributes:
        x -- x position of ship that raised exception
        y -- y position of ship that raised exception
    """

    def __init__(self, x, y, message=""):
        self.x = x
        self.y = y
        self.message = "Ships aren't on the right positions"
        super().__init__(message)
