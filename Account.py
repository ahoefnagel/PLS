class Account:
    def __init__(self, id, gender, name_set, given_name, surname, street_address, zipcode, city, email_address, username, telephone_number):
        self.id = id
        self.gender = gender
        self.name_set = name_set
        self.given_name = given_name
        self.surname = surname
        self.street_address = street_address
        self.zipcode = zipcode
        self.city = city
        self.email_address = email_address
        self.username = username
        self.telephone_number = telephone_number

    def __str__(self):
        return self.given_name + ' - ' + self.surname

    def to_msv(self):
        return ' - '.join([str(f) for f in self.__dict__.values()]) + '\n'

    def to_csv(self):
        return ','.join([str(f) for f in self.__dict__.values()]) + '\n'
