"""
Uses tkinter to make a search module that takes a Pokemon name and locates
their stats via PokeAPI
"""
import json
from tkinter import Tk, Label, Entry, Button
import requests


class Pokemon:
    """Class Pokemon takes a certain pokemons name, characteristics, and stats"""
    def __init__(self, attack, name, pokedex_number, type1, type2):
        self.attack = attack
        self.name = name
        self.pokedex_number = pokedex_number
        self.type1 = type1
        self.type2 = type2

    # formats Pokemon stat list
    def __str__(self):
        return f"name: {self.name}\nid: {self.pokedex_number}\n\
            type1: {self.type1}\ntype2: {self.type2}\nattack: {self.attack}"


class Pokedex:
    """Class Pokedex starts a tkinter GUI"""
    def __init__(self):
        self.root = Tk()

        self.enter_label = Label(text="Enter the name of the Pokemon")
        self.enter_entry = Entry()
        self.enter_button = Button(text="Retrieve Data")
        self.enter_button.bind("<Button-1>", self.clickhandler)  # signal to clickhandler method
        self.results_label = Label(text="")  # dynamic label that changes on user input

        self.enter_label.grid(row=0, column=0)
        self.enter_entry.grid(row=0, column=1)
        self.enter_button.grid(row=1, columnspan=2)
        self.results_label.grid(row=2, columnspan=2)

        self.root.mainloop()

    def clickhandler(self, _evt):
        """clickhandler method obtains name of entered Pokemon and tries to search PokeAPI"""
        name = self.enter_entry.get()  # obtains entry information
        try:
            self.search(str(name).lower())
        except ValueError as e:  # exceptions are printed if given
            self.results_label['text'] = e

    def search(self, name):
        """Searches and gets data of requested Pokemon from PokeAPI"""
        url = "https://pokeapi.co/api/v2/pokemon/" + name  # creates PokeAPI URL of desired Pokemon
        r = requests.get(url)  # checks to see if URL is valid

        if r.status_code != 200:  # if Pokemon isn't found with given name, ValueError is raised
            raise ValueError("Pokemon Not Found")

        else:  # if name is found, data is search for and assigned
            data = json.loads(r.text)
            name = data["name"]
            pokedex_number = data["id"]
            if len(data["types"]) == 1:
                type1 = data["types"][0]["type"]["name"]
                type2 = None
            else:
                type1 = data["types"][0]["type"]["name"]
                type2 = data["types"][1]["type"]["name"]
            for i in range(len(data["stats"])):
                if data["stats"][i]["stat"]["name"] == "attack":
                    attack = data["stats"][i]["base_stat"]

            # changes the dynamic label to a Pokemons information
            self.results_label["text"] = Pokemon(attack, name, pokedex_number, type1, type2)


Pokedex()  # starts Pokedex
