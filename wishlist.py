import json
import os


class WishList:

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    # ->dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
        }

    # dictionary->json
    @staticmethod
    def from_dict(data):
        return WishList(
            data["name"],
            data["price"]
        )


FILE_NAME = "wishlist.json"


def load_wishlist():
    wishlist = []

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
        for item in data:
            wishlist.append(WishList.from_dict(item))
    except FileNotFoundError:
        pass

    return wishlist


def save_wishlist(wishlist):
    data = []
    for item in wishlist:
        data.append(item.to_dict())
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def add_item(wishlist, name, price):
    item = WishList(name, price)
    wishlist.append(item)
    save_wishlist(wishlist)


def remove_item(wishlist, name, price):
    price_diff = 0
    for item in wishlist:
        if item.name == name:
            wishlist.remove(item)
            price_diff = price-item.price
            break
    save_wishlist(wishlist)
    return price_diff
