from exceptions.UnitException import UnitException


class MissingUnitException(UnitException):

    def __init__(self, error_message: str) -> None:
        super().__init__(error_message)
        return
