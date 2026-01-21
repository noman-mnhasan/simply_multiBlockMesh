

class PointTypeError(Exception):
    """ Raises error when invalid input is used to define a Point """
    def __init__(self, message, info):
        
        super.__init__(message)
        
        self.info = info


class MoveDefinitionError(Exception):
    """ Raises error when more than one move argument is provided """
    def __init__(self, message, info):
        
        super.__init__(message)
        
        self.info = info




