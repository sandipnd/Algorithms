class myExceptionCodes:
    INVALIDDATA = 1000


class myException(Exception):
    def __init__(self, message, type, parameters):
        self._message = message
        self.type = type

    def __str__(self):
        string = ''
        if self._message:
            string += self._message
        return string


class invalidDataException(myException):
    def __init__(self, message):
        self.message = message
        self.type =  myExceptionCodes.INVALIDDATA


class  processException(myException):
    def __init__(self, message):
        self.message = message
        self.type =  myExceptionCodes.INVALIDDATA


