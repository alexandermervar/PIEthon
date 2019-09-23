class user:
    def __init__(self, name, username, id):
        self.name = name
        self.username = username
        self.id = id

    def getName(self):
        return self.name

    def getUsername(self):
        return self.username

    def getId(self):
        return self.id