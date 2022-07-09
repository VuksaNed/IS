import copy
import math
import random

from agents import Agent


# Example agent, behaves randomly.
# ONLY StudentAgent and his descendants have a 0 id. ONLY one agent of this type must be present in a game.
# Agents from bots.py have successive ids in a range from 1 to number_of_bots.
class StudentAgent(Agent):
    def __init__(self, position, file_name):
        super().__init__(position, file_name)
        self.id = 0

    @staticmethod
    def kind():
        return '0'

    # Student shall override this method in derived classes.
    # This method should return one of the legal actions (from the Actions class) for the current state.
    # state - represents a state object.
    # max_levels - maximum depth in a tree search. If max_levels eq -1 than the tree search depth is unlimited.
    def get_next_action(self, state, max_levels):
        actions = self.get_legal_actions(state)  # equivalent of state.get_legal_actions(self.id)
        chosen_action = actions[random.randint(0, len(actions) - 1)]
        # Example of a new_state creation (for a chosen_action of a self.id agent):
        # new_state = state.apply_action(self.id, chosen_action)
        return chosen_action

#  python .\main.py maps\map4.txt ExpectAgent 10 -1

class MinimaxAgent(StudentAgent):

    def minimax(self, igrac, state, depth, max_levels):

        if igrac == "max":
            actions = self.get_legal_actions(state)
        else:
            actions = state.get_legal_actions(state.agents[1].id)

        if len(actions) == 0:
            if igrac == "max":
                return [-10000, None]
            else:
                return [10000, None]

        if depth == max_levels:
            s1 = 2 ** len(self.get_legal_actions(state))
            s2 = 2 ** len(state.get_legal_actions(state.agents[1].id))

            if igrac == "max":
                s1 = s1 - s2
            else:
                s1 = s2 - s1

            return [s1, None]

        if igrac == "max":
            score = [-math.inf, None]
            for akcije in actions:

                novostanje = state.apply_action(self.id, akcije)
                s = self.minimax("min", novostanje, depth + 1, max_levels)
                s[1] = akcije
                score = max(score, s, key=lambda a: a[0])

            return score
        else:
            score = [+math.inf, None]
            for akcije in actions:

                novostanje = state.apply_action(state.agents[1].id, akcije)
                s = self.minimax("max", novostanje, depth + 1, max_levels)
                s[1] = akcije
                score = min(score, s, key=lambda a: a[0])


            return score

    def get_next_action(self, state, max_levels):

        ret = self.minimax("max", state, 0, max_levels)
        if ret[1] is not None:
            return ret[1]
        else:
            actions = self.get_legal_actions(state)
            return actions[0]


class MinimaxABAgent(StudentAgent):

    def minimaxAB(self, igrac, state, depth, max_levels, a, b):

        if igrac == "max":
            actions = self.get_legal_actions(state)
        else:
            actions = state.get_legal_actions(state.agents[1].id)

        if len(actions) == 0:
            if igrac == "max":
                return [-10000, None]
            else:
                return [10000, None]

        if depth == max_levels:
            s1 = 2 ** len(self.get_legal_actions(state))
            s2 = 2 ** len(state.get_legal_actions(state.agents[1].id))

            if igrac == "max":
                s1 = s1 - s2
            else:
                s1 = s2 - s1

            return [s1, None]

        if igrac == "max":
            score = [-math.inf, None]
            for akcije in actions:

                novostanje = state.apply_action(self.id, akcije)
                s = self.minimaxAB("min", novostanje, depth + 1, max_levels, a, b)
                s[1] = akcije
                score = max(score, s, key=lambda aa: aa[0])
                a = max(a, score[0])
                if a >= b:
                    break

            return score
        else:
            score = [+math.inf, None]
            for akcije in actions:

                novostanje = state.apply_action(state.agents[1].id, akcije)
                s = self.minimaxAB("max", novostanje, depth + 1, max_levels, a, b)
                s[1] = akcije
                score = min(score, s, key=lambda aa: aa[0])
                b = min(b, score[0])
                if a >= b:
                    break

            return score

    def get_next_action(self, state, max_levels):
        ret = self.minimaxAB("max", state, 0, max_levels, - math.inf, math.inf)
        if ret[1] is not None:
            return ret[1]
        else:
            actions = self.get_legal_actions(state)
            return actions[0]


class ExpectAgent(StudentAgent):

    def expectimax(self, igrac, state, depth, max_levels):

        if igrac == "max":
            actions = self.get_legal_actions(state)
        else:
            actions = state.get_legal_actions(state.agents[1].id)

        if len(actions) == 0:
            if igrac == "max":
                return [-10000, None]
            else:
                return [10000, None]

        if depth == max_levels:
            s1 = 2 ** len(self.get_legal_actions(state))
            s2 = 2 ** len(state.get_legal_actions(state.agents[1].id))

            if igrac == "max":
                s1 = s1 - s2
            else:
                s1 = s2 - s1

            return [s1, None]

        if igrac == "max":
            score = [-math.inf, None]
            for akcije in actions:
                novostanje = state.apply_action(self.id, akcije)
                s = self.expectimax("chance", novostanje, depth + 1, max_levels)
                s[1] = akcije
                score = max(score, s, key=lambda a: a[0])

            return score
        else:
            score = [0, None]
            prob = 1 / len (actions)
            for akcije in actions:
                novostanje = state.apply_action(state.agents[1].id, akcije)
                s = self.expectimax("max", novostanje, depth + 1, max_levels)
                score[0] += prob * s[0]

            return score

    def get_next_action(self, state, max_levels):
        ret = self.expectimax("max", state, 0, max_levels)
        if ret[2 * self.id] is not None:
            return ret[1 + 2 * self.id]
        else:
            actions = self.get_legal_actions(state)
            return actions[0]


class MaxNAgent(StudentAgent):

    def minimaxn(self, igrac, state, depth, max_levels, ostaliigraci):

        actions = state.get_legal_actions(state.agents[igrac].id)

        if len(actions) == 0:
            ostaliigraci.append(igrac)
            if len(state.agents) == len(ostaliigraci) + 1:
                ret = []
                for i in range(len(state.agents)):
                    ret.append(-10000)
                    ret.append(None)
                i = 0
                while i in ostaliigraci:
                    i = i + 1
                ret[i * 2] = 10000
                return ret

            ig = (igrac + 1) % len(state.agents)
            while ig in ostaliigraci:
                ig = (ig + 1) % len(state.agents)
            s = self.minimaxn(ig, state, depth, max_levels, copy.deepcopy(ostaliigraci))
            s[1 + 2 * igrac] = None
            return s


        if depth == max_levels:
            ret = []
            for i in range(len(state.agents)):
                s1 = 2 ** len(state.get_legal_actions(state.agents[i].id))
                s2 = 0
                for j in range(len(state.agents)):
                    if i != j:
                        s2 = s2 + 2 ** len(state.get_legal_actions(state.agents[j].id))
                s2 = s2 / (len(state.agents) - 1)
                s1 = s1 - s2
                ret.append(s1)
                ret.append(None)

            return ret

        score = []
        for i in range(len(state.agents)):
            score.append(-math.inf)
            score.append(None)

        for akcije in actions:
            novostanje = state.apply_action(state.agents[igrac].id, akcije)
            ig = (igrac + 1) % len(state.agents)
            while ig in ostaliigraci:
                ig = (ig + 1) % len(state.agents)
            s = self.minimaxn(ig, novostanje, depth + 1, max_levels, copy.deepcopy(ostaliigraci))
            s[1 + 2 * igrac] = akcije
            score = max(score, s, key=lambda a: a[2 * igrac])

        return score

    def get_next_action(self, state, max_levels):
        ret = self.minimaxn(self.id, state, 0, max_levels, [])
        if ret[2 * self.id] is not None:
            return ret[1 + 2 * self.id]
        else:
            actions = self.get_legal_actions(state)
            return actions[0]
