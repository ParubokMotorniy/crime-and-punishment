from criminal import Criminal
from inspector import Inspector
import simulation_params
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys as sus

def update_simulation_params(new_g:int, new_p:int, new_k:int, new_r:int, new_randomness:float ):
    simulation_params.g = new_g
    simulation_params.p = new_p
    simulation_params.k = new_k
    simulation_params.r = new_r

    simulation_params.randomness_weight = new_randomness
    simulation_params.rationality_weight = 1.0 - simulation_params.randomness_weight

    simulation_params.s_i = simulation_params.k / simulation_params.r
    simulation_params.c_j = simulation_params.g / simulation_params.p

#num_criminals=num_inspectors
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

def plot_single_rate_progression(num_games:int, num_criminals:int, criminal_decision_function, inspector_decision_function, title):
    with sns.axes_style('darkgrid') and sns.color_palette('deep'):
    
        agent_randomness = [0.0, 0.2, 0.6, 1.0] 
        fig, ax = plt.subplots(nrows=2, ncols=len(agent_randomness))
        plt.subplots_adjust(wspace=0.8, hspace=0.8)

        #row, g,p
        parameters_setup = {'low_punishment':[0, 5, 6], 'high_punishment':[1, 5, 25]}

        fig.suptitle(title)

        for key,value in parameters_setup.items():
            row_idx = value[0]

            ax[row_idx][0].set_ylabel(key)

            for idx, randomness in enumerate(agent_randomness):
                simulation_params.randomness_weight = randomness
                update_simulation_params( value[1], value[2], simulation_params.k, simulation_params.r, randomness)
                
                rational_inspection_rates, rational_crime_rates = run_simulation(num_games, num_criminals, Criminal.if_commit_crime_rational, Inspector.if_inspect_rational)
                inspection_rates, crime_rates = run_simulation(num_games, num_criminals, criminal_decision_function, inspector_decision_function)
                
                df = pd.DataFrame.from_dict({"inspection_rates":inspection_rates, "crime_rates":crime_rates, "rational_inspection_rates":rational_inspection_rates, "rational_crime_rates":rational_crime_rates},orient='index')
                df['action_type'] = ['inspection', 'crime', 'inspection', 'crime']
                df['rationality_type'] = ['bounded', 'bounded', 'rational', 'rational']        
                df = df.melt(id_vars=['action_type', 'rationality_type'], value_name='mean_rate', var_name='game_idx')

                sns.lineplot(data=df, ax=ax[row_idx][idx], x='game_idx', y='mean_rate',legend='brief', hue='action_type', style='rationality_type')
                ax[row_idx][idx].set_title(f"{randomness*100}% random")
        
        handles, labels = ax[0][0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right')

        for i in range(len(agent_randomness)):
            for j in range(2):
                ax[j][i].get_legend().remove()

        plt.show()
        plt.clf()
        plt.cla()

def plot_rate_progression(num_games:int, num_criminals:int):
    plot_single_rate_progression(num_games, num_criminals,  Criminal.if_commit_crime_bounded_learning, Inspector.if_inspect_bounded_learning, "Bounded learning")
    plot_single_rate_progression(num_games, num_criminals,  Criminal.if_commit_crime_bounded_decision_making, Inspector.if_inspect_bounded_decision_making, "Bounded decision-making")


def plot_single_rate_matrix(num_games_per_point:int, num_agents:int, criminal_decision_function, inspector_decision_function, title):
    with sns.axes_style('darkgrid') and sns.color_palette('deep'):

        agent_randomness = np.linspace(0.0,1.0,20)
        utility_ratios = [0.05, 0.25, 0.5, 0.75, 0.95]
        fixed_kost = 5
        fixed_gain = 5

        print(agent_randomness)

        fig, ax = plt.subplots(nrows=len(utility_ratios), ncols=len(utility_ratios))
        plt.subplots_adjust(wspace=0.7, hspace=0.7)
        fig.suptitle(title)
        fig.supxlabel('Percentage of randomness in agent')
        fig.supylabel('Mean crime rate and inspection rate')

        for gain_idx in range(len(utility_ratios)-1, -1, -1): #indexes the row
            for kost_idx in range(len(utility_ratios)): #indexes the column
                mean_inspection_rates = []
                mean_crime_rates = []

                for randomness in agent_randomness:        
                    update_simulation_params( fixed_gain, max(1, int(float(fixed_gain) / utility_ratios[gain_idx])), fixed_kost, max(1, int(float(fixed_kost) / utility_ratios[kost_idx])), randomness)
                    inspection_rates, crime_rates = run_simulation(n_runs, n_agents, criminal_decision_function, inspector_decision_function)

                    mean_inspection_rates.append(np.mean(inspection_rates))
                    mean_crime_rates.append(np.mean(crime_rates))
                
                df = pd.DataFrame.from_dict({"mean_crime_rates":mean_crime_rates, "mean_inspection_rates":mean_inspection_rates})
                df.index = agent_randomness

                effective_row_idx = len(utility_ratios) - (gain_idx + 1)
                sns.lineplot(data=df, ax=ax[effective_row_idx][kost_idx], legend='brief')

                if gain_idx == 0:
                    ax[effective_row_idx][kost_idx].set_xlabel(f"K/R = {utility_ratios[kost_idx]}")

                if kost_idx == 0:
                    ax[effective_row_idx][kost_idx].set_ylabel(f"G/P = {utility_ratios[gain_idx]}")

            
        handles, labels = ax[0][0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right')

        for i in range(len(utility_ratios)):
            for j in range(len(utility_ratios)):
                ax[j][i].get_legend().remove()

        plt.show()
        plt.clf()
        plt.cla()

def plot_rate_matrices(num_games:int, num_criminals:int):
    plot_single_rate_matrix(num_games, num_criminals, Criminal.if_commit_crime_bounded_learning, Inspector.if_inspect_bounded_learning,"Bounded learning")
    plot_single_rate_matrix(num_games, num_criminals, Criminal.if_commit_crime_bounded_decision_making, Inspector.if_inspect_bounded_decision_making, "Bounded decision-making")

if __name__ == "__main__":
    n_runs = 1000
    n_agents = 1000

    plot_rate_progression(n_runs, n_agents)

    n_runs = 500
    n_agents = 100
    plot_rate_matrices(n_runs, n_agents)



