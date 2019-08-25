import uuid


def generate_id():
    """
    Generates a new UUID4 as a string
    """
    # uuid -> string issue
    # --------------------
    # https://stackoverflow.com/questions/47429929/attributeerror-uuid-object-has-no-attribute-replace
    return str(uuid.uuid4())
