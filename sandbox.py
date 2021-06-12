import random
from torch import optim
import torch
import torch.multiprocessing as mp
from AI.networks.actor_critic_network import ActorCriticNetwork


def train(model_g):
    # model_l = ActorCriticNetwork(input_size=1)
    # model_l.load_state_dict(model_g.state_dict())
    # optimizer = optim.Adam(model_g.parameters())
    # label = [random.randint(5, 15) for _ in range(10)]
    # for i in range(10):
    #     result = model_l.v(torch.Tensor([[[i]]]))
    #     loss = (label[i] - result) ** 2

    #     optimizer.zero_grad()
    #     loss.backward()
    #     for global_param, local_param in zip(model_g.parameters(), model_l.parameters()):
    #         global_param._grad = local_param.grad
    #     optimizer.step()
    #     print("ended")
    model_g.prii()


class momomo:
    def __init__(self) -> None:
        pass

    def prii(self):
        print("ggggg")


# if __name__ == "__main__":
#     num_processes = 4
#     model_g = ActorCriticNetwork(input_size=1)
#     model_g.share_memory()
#     momoin = momomo()

#     processes = []
#     for rank in range(num_processes):
#         p = mp.Process(target=train, args=(momoin,))
#         p.start()
#         processes.append(p)
#     for p in processes:
#         p.join()

import torch

print(torch.cuda.get_device_name())
print(torch.cuda.is_available())
