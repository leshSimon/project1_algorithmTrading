from AI.construction.atSimulation.stFinal_actorcritic_for_simulation import ActorCriticSimulation


class ActorCritic(ActorCriticSimulation):
    def __init__(self):
        super().__init__()

    def predict(self, situation):
        a_prob_serise = 0
        probability = max(a_prob_serise)
        act_index = a_prob_serise.index(probability)
        return act_index, probability

