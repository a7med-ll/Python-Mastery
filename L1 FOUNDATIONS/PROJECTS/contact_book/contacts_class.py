class Contact:
    def __init__(self, name, phonenum, email):
        self.name = name
        self.phonenum = phonenum
        self.email = email

    def __str__(self):
        return f"{self.name} | {self.phonenum} |  {self.email}"