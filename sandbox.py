import torch.multiprocessing as mp


class Model:
    def __init__(self, data) -> None:
        self.data = data

    def printing(self):
        print(f"self.data {self.data}")


def train(model):
    # Construct data_loader, optimizer, etc.
    for i in range(3):
        model.printing()


if __name__ == "__main__":
    num_processes = 4
    model = Model(12)
    processes = []
    for rank in range(num_processes):
        p = mp.Process(target=train, args=(model,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
