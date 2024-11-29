import simulation_constants
import numpy as np

class Criminal():
    def __init__(self) -> None:
        self.payoff = 0
    
    def if_commit_crime(self) -> bool:
        current_deciison = np.random.uniform(0.0,1.0)
        return current_deciison < simulation_constants.s_i
    
    def increase_payoff(self, increment: int) -> None:
        self.payoff += increment

    def get_payoff(self) -> int:
        return self.payoff

    def compute_payoff_rational(self, if_i_was_inspected:bool, if_i_robbed:bool, if_i_was_robbed:bool) -> int:
        gain = simulation_constants.g if if_i_robbed else 0
        inspection_loss = simulation_constants.p if if_i_was_inspected and if_i_robbed else 0
        robbed_loss = simulation_constants.l if if_i_was_robbed else 0
        return gain - inspection_loss - robbed_loss