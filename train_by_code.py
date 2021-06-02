from AI.pymon import PyMon


pymon = PyMon()


pymon.simulationInit(startDate=20190515)

while True:
    if pymon.mySituation[1] < pymon.today:
        pymon.simulation_at_one_point(learning=True)

