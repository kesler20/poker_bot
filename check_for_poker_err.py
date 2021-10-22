import random 
from random import randint
from immutable_poker_objects import *
from Applications.starting_projects.Engineering.data_processing import DataProcessing
dp = DataProcessing([])
import numpy as np
import pandas as pd 

class Node(object):
    
    def __init__(self, _type: str):
        self.history: list[list[Node]] = []
        self._type: str = _type # this can only be either action terminal or chance 
        self.players: list[Player] = []
        self.game_events: list = []
    
    def __str__(self):
        return ''

    def add_to_history(self, node):
        self.history.append([node])

    def info_set(self):
        information_set: list[int] = []
        for i in range(len(self.game_events)):
            if self.game_events[i] in self.history:
                information_set.append(i)
            else:
                self.history.append(self.game_events)
        return information_set
                   
class Table(object):
    
    def __init__(self, deck: list[Card], number_of_participants: int = 3):
        self.cards = list[Card] # list of cards on the table at time t  
        self.players_cards = [tuple] # tuples of record of which cards are owned by players
        self.players: list[Player] = []
        self.deck = deck
        self.number_of_participants : int = number_of_participants
        self.total_pot = 0
        self.minimum_bet = 1
    
    def create_random_players(self):
        for i in range(self.number_of_participants):
            player = Player(5000,[],i,self.minimum_bet,self.total_pot)
            self.players.append(player)

    def payout(self):
        players_points = [player.points for player in self.players]
        winner = [np.argmax(players_points)]
        if winner > 1:
            winners = winner
            high_cards = [player.cards for player in self.players]
            high_card = [np.argmax(high_cards)]
            for player in winners:
                player: Player
                players_cards = [cards for cards in player.cards]
                if high_card in players_cards:
                    winner = player
                else:
                    pass
        else:
            pass
        return winner, self.total_pot

    def shuffle_deck(self):
        shuffled_deck = random.shuffle(self.deck)
        return shuffled_deck

    def deal_to_participants(self):
        shuffled_deck = self.shuffle_deck()

        x = randint(0,len(shuffled_deck)-1)
        y = randint(0,len(shuffled_deck)-1)

        for _ in range(2):
            for participant in self.players:
                participant.cards(shuffled_deck[x],shuffled_deck[y])
                self.deck.remove(shuffled_deck[x],shuffled_deck[y])
            
    def pay(self, ammount, players):# only the players that have to pay the amount
        players: list[Player]
        for player in players:
            player.balance -= ammount
            self.total_pot += ammount
        
class Rules(Table):
    
    def __init__(self, players, cards, minimum_bet, total_pot):
        super().__init__(players, cards, minimum_bet, total_pot)

    def calculate_points(self):
        for player in self.players:
            self.pair_of_cards(player)
            self.double_pairs(player)
            self.three_of_a_kind(player)
            self.straight(player)
            self.flush(player)
            self.full_house()
            self.four_of_a_kind()
            self.straight_flush()
            self.ROYAL_FLUSH()

    def pair_of_cards(self,player):
        player: Player
        one_found = False
        cards: list[Card] = []
        cards.append(self.cards)
        cards.append(player)
        card_values = [card.value for card in cards]
        for card in cards:
            if card_values.count(card.value) == 2:
                player.points = 2
                one_found = True
            else:
                pass
        return one_found

    def double_pairs(self):
        one_found = False
        for i in range(len(self.players)):
            cards: list[Card] = []
            cards.append(self.cards)
            player = self.players[i]
            cards.append(player)
            card_values = [card.value for card in cards]
            for card in cards:
                if card_values.count(card.value) == 2 and one_found:
                    one_found = True
                    player.points = 3
                else:
                    pass

    def three_of_a_kind(self, player):
        player: Player
        one_found = False
        cards: list[Card] = []
        cards.append(self.cards)
        cards.append(player)
        card_values = [card.value for card in cards]
        for card in cards:
            if card_values.count(card.value) == 3:
                player.points = 4
                one_found = True
            else:
                pass
        return one_found

    def straight(self, player):
        player: Player
        _straight = False
        cards: list[Card] = []
        cards.append(self.cards)
        cards.append(player)
        card_values = [card.value for card in cards]
        possible_sequences = []
        for card_val in card_values:
            possible_sequences.append(card_sequence1 = [card_val + i for i in range(5)])
            possible_sequences.append(card_sequence2 = [card_val - i for i in range(5)])
            for x in range(5):
                card_sequence3 = [card_val + i for i in range(5 - x)]
                card_sequence3.append(card_val - x)
                possible_sequences.append(card_sequence3)
        for sequence in possible_sequences:
            if sequence in card_values:
                player.points = 5
                print(sequence)
                _straight = True
            else:
                pass
        return _straight

    def flush(self, player):
        player: Player
        _flush = False
        cards: list[Card] = []
        cards.append(self.cards)
        cards.append(player)
        card_suits = [card.value for card in cards]
        for card in cards:
            if card_suits.count(card.value) == 5:
                player.points = 6 
                _flush = True
            else:
                pass
        return _flush

    def full_house(self):
        for player in self.players:
            three_of_knd = self.three_of_a_kind(player)
            pair = self.pair_of_cards(player)
            if three_of_knd and pair:
                player.points = 7
            else:
                pass
            

    def four_of_a_kind(self):
        for i in range(len(self.players)):
            cards: list[Card] = []
            cards.append(self.cards)
            player = self.players[i]
            cards.append(player)
            card_values = [card.value for card in cards]
            for card in cards:
                if card_values.count(card.value) == 4:
                    player.points = 8
                else:
                    pass    
        
    def straight_flush(self):
        for player in self.players:
            f = self.flush(player)
            s = self.straight(player)
            if f and s:            
                player.points = 9
            else:
                pass

    def ROYAL_FLUSH(self):
        for player in self.players:
            f = self.flush(player)
            if f:
                cards: list[Card] = []
                cards.append(self.cards)
                cards.append(player)
                card_values = [card.value for card in cards]
                highest_sequence = [10, 11, 12, 13, 'A']
                if highest_sequence in card_values:
                    player.points = 10
                else:
                    pass
            else:
                pass

class Player(Rules):
    
    def __init__(self, balance: int, cards: list[Card], _id: int, minimum_bet: int, total_pot: int):
        super().__init__(minimum_bet, total_pot)
        self.balance: int = balance 
        self.cards: list = cards
        self._id: int = _id
        self.points: int = self.calculate_points(cards)
        self.strategy_buleprint = self.strategy_blueprint()
        self.regret_table = self.init_regret_table(self)
    
    def __str__(self):
        return f'''
            Player {self._id} (
                blance : {self.balance},
                cards : ({self.cards[0]}, {self.cards[1]}),
            )
        '''
    def init_regret_table(self):
        reward = -1*self.minimum_bet
        df = dp.dataframe_generator(
            Iteration=[1], 
            raise_bet=[self.minimum_bet*(1 + self.full_kelly_criterion(0.5)) - reward],
            check=[self.minimum_bet - reward],
            fold=[-1*self.minimum_bet - reward]
            )
        print(f'''
        ----------------Regret Table--------------------: 

        {df}
        ''')
        return df
    
    def arg_max(self, action_space):
        max_value = 0
        for value in action_space:
            if value > max_value:
                max_value = value
            else:
                pass

        return max_value

    def strategy_blueprint(self,information_set):
        regret_table = self.init_regret_table()
        columns = dp.series_to_list(regret_table.columns)
        columns.remove('Iteration')

        probabilities_of_actions = []
        regrets = []
        for col in columns:
            regrets.append(regret_table[col])
        total_regrets = sum(regrets)
        for column in columns:
            reward = regret_table[column]
            confidence = reward/total_regrets
            probabilities_of_actions.append((column, confidence[0]))
        
        confidences = []
        for action, confidence in probabilities_of_actions:
            confidences.append(confidence)
            print(action, confidence)
            best_action = self.arg_max(confidences)
            if confidence == best_action:
                best_action = action
                if best_action == 'raise_bet':
                    best_action = ('raise bet', confidence)
                break
            else:
                pass
            print(best_action)
        
        strategy = {
            'information set': information_set,
            'actions' : [best_action]
        }
        df = pd.DataFrame(strategy)
        print(f'''
        ----------------Strategy Tabke--------------------: 

        {df}
        ''')
        return df

    def calculate_points(self):
        return super().calculate_points()
    
    def calculate_odds(self):
        return self.total_pot/self.minimum_bet
    
    def full_kelly_criterion(self, confidence):
        odds = self.calculate_odds()
        pw = confidence 
        pl = 1 - pw
        lot_size = (odds*confidence - pl)/odds
        return lot_size
    
class Game(Rules):
    
    def __init__(self, deck, number_of_participants):
        super().__init__(deck, number_of_participants)

    def ante(self,tbl: Table):
        tbl.pay(tbl.minimum_bet,tbl.players)
        return tbl

    def start(self):
        deck = PokerDeck()
        deck = deck.initialize_deck()
        tbl = Table(deck,3)
        tbl.create_random_players()
        tbl.deal_to_participants()
        tbl.deck = tbl.shuffle_deck()
        return deck, tbl

    def betting_round(self,tbl: Table):
        for player in tbl.players:
            action = player.strategy_blueprint([1])
            if action['action'] == 'fold':
                tbl.players.remove(player)
            elif action['action'] == 'check':
                player.pay(self.minimum_bet,[player])
            else:
                raising_ammount = self.minimum_bet*(1 + player.full_kelly_criterion(action['action'][0][1]))
                player.pay(raising_ammount,[player])
                tbl.minimum_bet += raising_ammount
        return tbl.players # make the betting rouynd end only when everyone has bet at least the minimum bet using a while loop
 
    def flop(self, tbl: Table):
        tbl.deck.remove(tbl.deck[0])
        for i in range(3):
            tbl.cards.append(tbl.deck[i])
            tbl.deck.remove(tbl.deck[i])
        return tbl

    def turn(self, tbl: Table):
        tbl.deck.remove(tbl.deck[0])
        tbl.cards.append(tbl.deck[1])
        tbl.deck.remove(tbl.deck[1])
        return tbl

    def river(self, tbl: Table):
        tbl.deck.remove(tbl.deck[0]) 
        tbl.cards.append(tbl.deck[1])
        tbl.deck.remove(tbl.deck[1])
        return tbl

    def evaluate(self, tbl: Table):
        winner, reward = tbl.payout()
        for player in tbl.players:
            if player._id == winner._id:
                player.balance += reward
        return tbl 
    
'''

from check_for_poker_err import *

deck = PokerDeck().initialize_deck()
print(deck)
tbl = Table(deck)
tbl.create_random_players()
gm = Game()
root = Node('chance')
root.game_events.append([gm.ante(),tbl.pay(1,tbl.players)])
root.game_events.append([gm.start(), tbl.deal_to_participants()])
branch = Node('action')
branch.game_events.append([gm.betting_round(),gm.flop()])

'''