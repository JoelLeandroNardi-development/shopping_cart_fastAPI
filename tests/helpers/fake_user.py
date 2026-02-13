class FakeUser:
    def __init__(self, name: str = None, phone_number: str = None):
        self.id = None
        self.name = name
        self.phone_number = phone_number

    def update(self, name: str, phone_number: str):
        if not name.strip():
            raise ValueError("Name is required")
        self.name = name
        self.phone_number = phone_number
