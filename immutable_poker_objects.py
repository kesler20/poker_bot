from dataclasses import dataclass, field
import pandas as pd 
    
@dataclass(order=True)
class Card(tuple):

    sort_index: int = field(init=False, repr=False)
    value: int
    suit: str
    
    def __post_init__(self):
        self.sort_index = self.value

    def __get__(self, instance, owner):
        return (self.value,self.suit)
    
    def __repr__(self):
        return f'''
            Card({self.value}, {self.suit})
        '''

class PokerDeck(list):
    
    def __init__(self):
        self.deck = self.initialize_deck()
    
    def __len__(self):
        return len(self.deck)
    
    def __str__(self):
        return f'''
        {self.deck}
        '''

    def initialize_deck(self):
        deck: list[Card] = []
        values = [val for val in range(2,14)]
        suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
        for i in suits:
            ace_card = Card(value='A',suit=i)
            for j in values:
                card = Card(value=j,suit=i)
                deck.append(card)
                if ace_card not in deck:
                    deck.append(ace_card)
                else:
                    pass
        return deck

