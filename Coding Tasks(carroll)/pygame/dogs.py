class Dog():
    def __init__ (self,name,colour):
        self.name = name
        self.colour = colour
    def set_colour(self,my_colour):
        self.colour = my_colour
    def get_colour():
        return self.colour

my_dog1 = Dog("Fido","Brown")
my_dog2 = Dog("Rex","Black")

print(my_dog1.name,my_dog1.colour)
print(my_dog2.name,my_dog2.colour)
