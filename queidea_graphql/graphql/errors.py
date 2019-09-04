class GenericError(Exception):
    def __init__(self, message="Invalid data", code="NEPTUNE_ERROR_GENERIC", payload=None):
        Exception.__init__(self)
        self.message = message
        self.code = code
        self.payload = payload

    def to_dict(self):
        error_list = dict(self.payload or ())
        error = {
            "errors": error_list,
            "status": "error",
            "message": self.message
        }
        return error
