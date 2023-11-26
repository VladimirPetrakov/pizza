class CustomException(Exception):

    def __init__(self, message):
        self.message = message


class InvalidCountCityBlocksDirectionException(CustomException):

    def __init__(self, count_blocks, max_count_blocks_direction):
        message = 'Invalid count of the city blocks = {}.'
        message += ' The count of the city blocks mush be positive and less than or equal to {}'

        message.format(count_blocks, max_count_blocks_direction)

        super().__init__(message)


class InvalidCountPizzeriasException(CustomException):

    def __init__(self, count, max_count):
        message = 'Invalid count of the pizzerias = {}.'
        message += ' The count of the pizzerias must be positive and less than or equal to {}'

        message.format(count, max_count)

        super().__init__(message)


class InvalidCoordinateBlockException(CustomException):

    def __init__(self, coordinate, max_coordinate):
        message = 'Invalid coordinate of the block = {}.'
        message += ' The coordinate of the block must be positive and less than or equal to {}'

        message.format(coordinate, max_coordinate)

        super().__init__(message)


class ImpossibleAppointBlocksException(CustomException):

    def __init__(self):
        message = 'Impossible to appoint blocks'

        super().__init__(message)
