class Chat:

    def __init__(
        self,
        id: int,
        message: str,
        response: str
    ):

        self.id = id
        self.message = message
        self.response = response

    def to_dict(self):

        return {
            "id": self.id,
            "message": self.message,
            "response": self.response
        }