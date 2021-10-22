import pandas as pd
from Applications.starting_projects.Engineering.data_processing import DataProcessing
dp = DataProcessing([])
minimum_bet = 2
total_pot = 6
reward = -1
import numpy as np

def arg_max(action_space):
    max_value = 0
    for value in action_space:
        if value > max_value:
            max_value = value
        else:
            pass

    return max_value
def init_regret_table():
    df = dp.dataframe_generator(
        Iteration=[1], 
        raise_bet=[minimum_bet*(1 + full_kelly_criterion(0.5)) - reward],
        check=[minimum_bet - reward],
        fold=[-1*minimum_bet - reward]
        )
    return df

def strategy_blueprint(information_set):
    regret_table = init_regret_table()
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
        best_action = arg_max(confidences)
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
    return df

def calculate_odds():
    return total_pot/minimum_bet

def full_kelly_criterion(confidence):
    odds = calculate_odds()
    pw = confidence 
    pl = 1 - pw
    lot_size = (odds*confidence - pl)/odds
    return lot_size

regret_table = init_regret_table()
print(f'''
----------------Regret Table--------------------: 

{regret_table}
''')

strategy = strategy_blueprint([1])
print(f'''
----------------Strategy Tabke--------------------: 

{strategy}
''')
#you will use the information set as the index of which action to take when the player is asked to act 
# build different workflows and coroutines in check error files to see 
# that each moving part of the system works