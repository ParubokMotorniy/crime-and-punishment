import simulation_params
import numpy as np

class Inspector():
    def __init__(self) -> None:
        self.payoff = 0
        self.detection_memory = [1]
        self.num_inspections = 1
        self.rational_detection_estimate = np.mean(self.detection_memory)
    
    def if_inspect_rational(self) -> bool:
        current_deciison = np.random.uniform(0.0,1.0)
        return current_deciison <= simulation_params.c_j

    def if_inspect_bounded_learning(self) -> bool:
        random_guess_probability_estimate_noise = np.random.uniform(0.0,1.0)

        estimated_reward_probability = (simulation_params.rationality_weight * self.rational_detection_estimate + simulation_params.randomness_weight * random_guess_probability_estimate_noise)

        # print(f"history estimate: {self.rational_detection_estimate}")
        # print(f"probability noise: {random_guess_probability_estimate_noise}")
        # print(f"reward prob: {estimated_reward_probability}")

        return estimated_reward_probability * float(simulation_params.r) > simulation_params.k

    def if_inspect_bounded_decision_making(self) -> bool:
        random_guess_probability_estimate_noise = np.random.uniform(-1.0,1.0)

        rational_payoff_estimate = self.rational_detection_estimate * simulation_params.r - simulation_params.k
        standardization_scale = (simulation_params.r - simulation_params.k) if rational_payoff_estimate > 0 else (- simulation_params.k) #reward is always larger then inspection cost
        return simulation_params.rationality_weight * float((abs(rational_payoff_estimate) / float(standardization_scale))) + simulation_params.randomness_weight * random_guess_probability_estimate_noise > 0 

    def update_payoff(self, if_i_inspected:bool, if_my_inspectee_commited_crime:bool):
        inspection_loss = simulation_params.k if if_i_inspected else 0
        inspection_gain = simulation_params.r if if_i_inspected and if_my_inspectee_commited_crime else 0
        
        payoff_increment = inspection_gain - inspection_loss 
        self.payoff += payoff_increment

        self.detection_memory.append(1 if if_my_inspectee_commited_crime else 0)
        self.rational_detection_estimate = np.mean(self.detection_memory[(len(self.detection_memory) - min(simulation_params.agent_memory_length, len(self.detection_memory))):])

        if if_i_inspected:
            self.num_inspections += 1

        return payoff_increment
    
    def get_payoff(self) -> int:
        return self.payoff
    
    def get_num_detections(self):
        return self.num_inspections