import simulation_constants
import numpy as np

class Criminal():
    def __init__(self) -> None:
        self.payoff = 0
        self.detection_memory = [0]
        self.num_crimes = 1
        self.rational_detection_estimate = np.mean(self.detection_memory)
    
    def if_commit_crime_rational(self) -> bool:
        current_deciison = np.random.uniform(0.0,1.0)
        return current_deciison <= simulation_constants.s_i
    
    def if_commit_crime_bounded_learning(self) -> bool:
        random_detection_probability_estimate_noise = np.random.uniform(0.0,1.0)

        punishment_probability = (simulation_constants.rationality_weight * self.rational_detection_estimate + simulation_constants.randomness_weight * random_detection_probability_estimate_noise)

        # print(f"history estimate: {self.rational_detection_estimate}")
        # print(f"probability noise: {random_detection_probability_estimate_noise}")
        # print(f"punishment prob: {punishment_probability}")

        return simulation_constants.g > float(simulation_constants.p) * punishment_probability

    def if_commit_crime_bounded_decision_making(self) -> bool:
        random_detection_probability_estimate_noise = np.random.uniform(-1.0,1.0)

        rational_payoff_estimate = int(simulation_constants.g - float(simulation_constants.p) * self.rational_detection_estimate)
        standardization_scale = simulation_constants.g if rational_payoff_estimate > 0 else (simulation_constants.g - simulation_constants.p) #punishment is always greater than gain
        return simulation_constants.rationality_weight * float((abs(rational_payoff_estimate) / float(standardization_scale))) + simulation_constants.randomness_weight * random_detection_probability_estimate_noise > 0

    def update_payoff(self, if_i_was_inspected:bool, if_i_robbed:bool, if_i_was_robbed:bool) -> int:
        gain = simulation_constants.g if if_i_robbed else 0
        inspection_loss = simulation_constants.p if if_i_was_inspected and if_i_robbed else 0
        robbed_loss = simulation_constants.l if if_i_was_robbed else 0

        payoff_increment = gain - inspection_loss - robbed_loss
        self.payoff += payoff_increment

        self.detection_memory.append(1 if if_i_was_inspected else 0)
        self.rational_detection_estimate = np.mean(self.detection_memory[(len(self.detection_memory) - min(simulation_constants.agent_memory_length, len(self.detection_memory))):])

        if if_i_robbed:
            self.num_crimes += 1

        return payoff_increment
    
    def get_payoff(self) -> int:
        return self.payoff
    
    def get_num_crimes(self):
        return self.num_crimes