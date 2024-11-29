from inspectee import Criminal
from inspector import Inspector
import simulation_constants
import sys as sus

def run_simple_simulation(num_games:int):
    criminal1 = Criminal()
    inspector1 = Inspector()

    criminal2 = Criminal()
    inspector2 = Inspector()

    criminal_decisions = []
    inspector_decisions = []

    for game in range(num_games):
        id1 = inspector1.if_inspect()
        id2 = inspector2.if_inspect()

        cd1 = criminal1.if_commit_crime()
        cd2 = criminal2.if_commit_crime()

        pi1 = inspector1.compute_payoff_rational(id1,cd1)
        inspector1.increase_payoff(pi1)

        pi2 = inspector2.compute_payoff_rational(id2,cd2)
        inspector2.increase_payoff(pi2)

        cp1 = criminal1.compute_payoff_rational(id1,cd1,cd2)
        criminal1.increase_payoff(cp1)

        cp2 = criminal2.compute_payoff_rational(id2,cd2,cd1)
        criminal2.increase_payoff(cp2)

        inspector_decisions.append((id1, id2))
        criminal_decisions.append((cd1, cd2))

    print(f"Criminal 1 payoff: {criminal1.get_payoff()}")
    print(f"Criminal 2 payoff: {criminal2.get_payoff()}")
    print(f"Inspector 1 payoff: {inspector1.get_payoff()}")
    print(f"Inspector 2 payoff: {inspector2.get_payoff()}")

    return inspector_decisions, criminal_decisions

if __name__ == "__main__":
    print(f"Crime probability: {simulation_constants.s_i}")
    print(f"Inspection probability: {simulation_constants.c_j}")
    inspection_decisions, crime_decisions = run_simple_simulation(int(sus.argv[1]))


