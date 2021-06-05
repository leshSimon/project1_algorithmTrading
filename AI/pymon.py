from AI.construction.atReal.actor_critic import ActorCritic


class PyMon(ActorCritic):
    """
      이 클래스 모듈은 인공지능 동작에 대한 API를 제공한다.
      클래스는 다음과 같이 위에서 아래로 상속된다.

      ActorCriticSimulation
      ActorCritic
      PyMon
      
    """

    def __init__(self):
        super().__init__()

