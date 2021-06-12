import random
from torch import optim
import torch
import torch.multiprocessing as mp
from AI.networks.actor_critic_network import ActorCriticNetwork


def train(name, device, q1, q2):
    model_l = ActorCriticNetwork(input_size=1).to(device)
    # model_l.load_state_dict(model_g.state_dict())
    model_l.load_state_dict(torch.load("networkWeights.pt"))
    optimizer = optim.Adam(model_l.parameters())
    label = [random.randint(5, 15) for _ in range(10)]
    for i in range(10):
        model_l.load_state_dict(torch.load("networkWeights.pt"))
        result = model_l.v(torch.Tensor([[[i]]]).to(device))
        loss = (label[i] - result) ** 2

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        st = f"{name}: steped"
        # print(f"{name}: steped")
        q1.put(st)
    q2.put("ended")


def learner(q1, q2):
    while q2.qsize() < 3:
        pass
    print("ended so start")
    while q1.qsize() > 0:
        print(q1.get())


if __name__ == "__main__":
    names = ["학생1", "학생2", "학생3"]
    device = torch.device("cuda")
    model_g = ActorCriticNetwork(input_size=1).to(device)
    torch.save(model_g.state_dict(), "networkWeights.pt")
    q1 = mp.Queue()
    q2 = mp.Queue()

    processes = []
    p = mp.Process(target=learner, args=(q1, q2))
    p.start()
    processes.append(p)
    for name in names:
        p = mp.Process(target=train, args=(name, device, q1, q2))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

