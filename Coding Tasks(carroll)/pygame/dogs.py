class Dog():
    def __init__ (self,name,colour):
        self.name = name
        self.colour = colour
    def set_colour(self,my_colour):
        self.colour = my_colour
    def get_colour():
        return self.colour

class Puppy(Dog):
    def __init__ (self, name, colour):
        super().__init__(name, colour)
        self.shoesChewed = 0
    def chewShoe(self, numShoes):
        self.shoesChewed += numShoes
    def getShoes(self):
        return self.shoesChewed

my_dog1 = Dog("Fido","Brown")
my_dog2 = Dog("Rex","Black")

my_pappy1 = Puppy("Dave","Purple")

my_pappy1.chewShoe(3)

print(my_pappy1.name,my_pappy1.colour,my_pappy1.getShoes())

print(my_dog1.name,my_dog1.colour)
print(my_dog2.name,my_dog2.colour)
