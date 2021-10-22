from random import randint
from Applications.starting_projects.Engineering import data_processing as dp
import random



class PokerBot(object):

    def __init__(self, number_of_participants, capital=0, number_of_games=0):
        self.number_of_participants = number_of_participants     
        self.capital = capital
        self.number_of_games = number_of_games
    
            
    def simulate_game(self):
        processing = dp.DataProcessing(self.initialize_deck())
        
        _ , Table = self.deal_to_participants() 
        Complete_table = []
        pot = []
        flop = self.deal_cards_on_table(3)
        turn = self.deal_cards_on_table(1)
        river = self.deal_cards_on_table(1)

        Complete_table.append(flop)
        Complete_table.append(turn)
        Complete_table.append(river)
        Complete_table = processing.series_to_list(Complete_table)
        print(Complete_table)

        flush = []
        straight = []
        pair = []
        double_pair = []
        Complete_table_numbers = []
        for i in Complete_table:
            if i[0].startswith('A'):
                p = 1
            elif i[0].startswith('J'):
                p = 11
            elif i[0].startswith('Q'):
                p = 12
            elif i[0].startswith('K'):
                p = 13
            else:
                p = i[0]
            Complete_table_numbers.append(p)
        for i in range(self.number_of_participants):
            if Table[f'participant {i}'][0] or Table[f'participant {i}'][1] in Complete_table:
                pair.append(i)
            elif Table[f'participant {i}'][0] and Table[f'participant {i}'][1] in Complete_table:
                double_pair.append(i)
            else:
                pass

