from AI.pymon import PyMon


pymon = PyMon()


pymon.simulationInit(startDate=20190515)

while True:
    pymon.simulation_at_one_point(learning=True)
