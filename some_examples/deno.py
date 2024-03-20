import pyjokes


def get_joke():
    joke = pyjokes.get_joke(language="en")
    print(joke)


from utility import *  # divide, multiply
from shopping.more_shopping import shopping_cart

print(shopping_cart.buy("test"))
print(divide(5, 2))
print(multiply(5, 2))

if __name__ == "__main__":
    print("it's the root file")


get_joke()
