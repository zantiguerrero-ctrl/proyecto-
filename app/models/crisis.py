class CrisisAlert:

    def __init__(
        self,
        id: int,
        user_id: int,
        level: str,
        description: str
    ):

        self.id = id
        self.user_id = user_id
        self.level = level
        self.description = description

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "level": self.level,
            "description": self.description
        }