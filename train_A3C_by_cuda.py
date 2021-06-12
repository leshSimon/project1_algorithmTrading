import torch
from AI.pymon import PyMon
import torch.multiprocessing as mp


def actor_run(actor_name: str, actor_id: int, device, observed_container, actors_act_container):
    db_name = "selected_by_code" + str(actor_id + 1)
    queues_for_multiprocessing = {
        "observed_container": observed_container,
        "actors_act_container": actors_act_container,
    }
    network_local = PyMon(
        name=actor_name,
        target_database_name=db_name,
        device=device,
        queues_for_multiprocessing=queues_for_multiprocessing,
    )
    network_local.simulationInit(startDate=20190515)

    first_data = []
    while first_data == []:
        first_data = network_local.make_input_state_for_AI_in_simulation()
        network_local.momentMovementForward()

    first_input = [actor_id + 1, 0, first_data.numpy()]
    print(first_input)
    observed_container.put(first_input)
    print("bgfbgbfgdbfgbfgbdbfgdbgd")

    while network_local.mySituation[1] < network_local.today:
        if actors_act_container.qsize() > 0:
            network_local.simulation_at_one_point()
            print(f"{actor_name} acted")


def learner_run(device, observed_container, actors_act_containers):
    Learner = PyMon(name="Learner", device=device)
    actors_count = len(actors_act_containers)
    pastRecords = [0 for _ in range(actors_count)]
    while True:
        if observed_container.qsize() > 0:
            [actorNum, reward, result] = observed_container.get()
            result = torch.Tensor(result)
            idx = actorNum - 1
            if pastRecords[idx] != 0:
                [result_past, pi] = pastRecords[idx]
                print("bbbbbbbbbbbbbbbb")
                Loss = Learner.loss_calculate(reward, result_past, result, pi)
                Learner.weight_update_in_simulation(Loss)
                print("hhhhhhhhhhhhhhhhhhhhhh")
            print("dddddddddddddddddddddddddddd")
            next_act = Learner.inference_in_simulation(result)
            print("5555555555555555555555555")
            pastRecords[idx] = [result, next_act]
            [act_idx, _] = next_act
            print(act_idx)
            actors_act_containers[idx].put([act_idx, 0])
            print(f"Learner is learning at env {actorNum}")


if __name__ == "__main__":
    actors = ["Actor_1"]
    device = torch.device("cuda")

    observed_container = mp.Queue()  # [행위자 번호, 보상, 결과]
    actors_act_containers = [mp.Queue() for _ in range(len(actors))]

    print("MP start method:", mp.get_start_method())

    processes = []
    p = mp.Process(target=learner_run, args=(device, observed_container, actors_act_containers))
    p.start()
    processes.append(p)
    for actor_id, name in enumerate(actors):
        p = mp.Process(
            target=actor_run, args=(name, actor_id, device, observed_container, actors_act_containers[actor_id])
        )
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

