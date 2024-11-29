import simulation_constants
import numpy as np

class Inspector():
    def __init__(self) -> None:
        self.payoff = 0
    
    def if_inspect(self) -> bool:
        current_deciison = np.random.uniform(0.0,1.0)
        return current_deciison < simulation_constants.c_j
    
    def increase_payoff(self, increment: int) -> None:
        self.payoff += increment

    def get_payoff(self) -> int:
        return self.payoff

    def compute_payoff_rational(self, if_i_inspected:bool, if_i_guessed:bool):
        inspection_loss = simulation_constants.k if if_i_inspected else 0
        inspection_gain = simulation_constants.r if if_i_inspected and if_i_guessed else 0

        return inspection_gain - inspection_loss
    