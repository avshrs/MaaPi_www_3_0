class Person:
    def __init__(self, name, job=None, pay=0):
        self.name = name
        self.job = job
        self.pay = pay
    def lastName(self):
        return self.name.split()[-1]
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))
    def __str__(self):
        return '[Person: %s, %s]' % (self.name, self.pay)

class Manager:
    def __init__(self, name, pay):
        self.person = Person(name, 'manager', pay) # Osadzenie obiektu Person
    def giveRaise(self, percent, bonus=.10):
        self.person.giveRaise(percent + bonus) # Przechwycenie i delegowanie
    def __getattr__(self, attr):
        return getattr(self.person, attr) # Delegowanie wszystkich pozostałych atrybutów
    def __str__(self):
        return str(self.person) # Musi

class Department:
    def __init__(self, *args):
        self.members = list(args)
    def addMember(self, person):
        self.members.append(person)
    def giveRaises(self, percent):
        for person in self.members:
            person.giveRaise(percent)
    def showAll(self):
        for person in self.members:
            print(person)

if __name__ == '__main__':
    bob = Person('Robert Zielony')
    anna = Person('Anna Czerwona', job='programista', pay=100000)
    print(bob)
    print(anna)
    print(bob.lastName(), anna.lastName())
    anna.giveRaise(.10)
    print(anna)
    tom = Manager('Tomasz Czarny', 50000) # Utworzenie obiektu Manager: __init__
    tom.giveRaise(.10) # Wykonanie własnej wersji
    print(tom.lastName()) # Wykonanie odziedziczonej metody
    print(tom)
    print('--Wszystkie trzy--')
    for object in (bob, anna, tom): # Ogólne przetwarzanie obiektów
        object.giveRaise(.10) # Wykonanie metody giveRaise tego obiektu
        print(object)

    development = Department(bob, anna) # Osadzenie obiektów w kompozycie
    development.addMember(tom)
    development.giveRaises(.10) # Wykonuje metodę giveRaise osadzonych obiektów
    print ("dupa")
    development.showAll()
    import shelve
    db = shelve.open('persondb') # Nazwa pliku, w którym przechowywane są obiekty
    for object in (bob, anna, tom): # Użycie atrybutu name obiektu jako klucza
        db[object.name] = object # Przechowanie obiektu w pliku shelve po kluczu
    db.close()
