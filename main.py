from criminal import Criminal
from inspector import Inspector
import simulation_constants
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys as sus

def run_simulation(num_games:int, num_criminals:int, criminal_decision_function, inspector_decision_function):
    criminals = [Criminal() for i in range(num_criminals)]
    inspectors = [Inspector() for i in range(num_criminals)]
    
    averaged_inspection_rates = []
    averaged_crime_rates = []

    for game_idx in range(1,num_games+1):
        random_game_groups = [i for i in range(num_criminals)]
        np.random.shuffle(random_game_groups)

        game_inspection_rates = []
        game_crime_rates = []

        for group_idx in range(0,len(random_game_groups),2):
            inspector1 = inspectors[group_idx]
            inspector2 = inspectors[group_idx+1]

            id1 = inspector_decision_function(inspector1)
            id2 = inspector_decision_function(inspector2)

            criminal1 = criminals[group_idx]
            criminal2 = criminals[group_idx + 1]

            cd1 = criminal_decision_function(criminal1)
            cd2 = criminal_decision_function(criminal2)

            inspector1.update_payoff(id1, cd1)
            inspector2.update_payoff(id2, cd2)

            criminal1.update_payoff(id1, cd1, cd2)
            criminal2.update_payoff(id2, cd2, cd1)

            game_inspection_rates.append(inspector1.get_num_detections() / game_idx)
            game_inspection_rates.append(inspector2.get_num_detections() / game_idx)

            game_crime_rates.append(criminal1.get_num_crimes() / game_idx)
            game_crime_rates.append(criminal2.get_num_crimes() / game_idx)

        averaged_inspection_rates.append(np.mean(game_inspection_rates))
        averaged_crime_rates.append(np.mean(game_crime_rates))

    return averaged_inspection_rates, averaged_crime_rates

if __name__ == "__main__":
    n_runs = 1000
    n_agents = 500

    inspection_rates, crime_rates = run_simulation(n_runs, n_agents, Criminal.if_commit_crime_bounded_learning, Inspector.if_inspect_bounded_learning)
    rational_inspection_rates, rational_crime_rates = run_simulation(n_runs, n_agents, Criminal.if_commit_crime_rational, Inspector.if_inspect_rational)

    dataframe = pd.DataFrame.from_dict({"inspection_rates":inspection_rates[9:], "crime_rates":crime_rates[9:],"rational_inspection_rates":rational_inspection_rates[9:], "rational_crime_rates":rational_crime_rates[9:]})

    fig,ax = plt.subplots()
    plt.style.use('_mpl-gallery')
    sns.set_theme()
    sns.lineplot( data=dataframe,ax=ax)

    plt.show()


