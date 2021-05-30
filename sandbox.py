# from stock_API.deashinAPI.market import kospi_Top_N_from_database
# # from AI.networks.actor_critic import ActorCritic
# from stock_API.kiwoomAPI.initiate import version_up_to_date
# from stock_API.deashinAPI.db_API import *
# from stock_API.deashinAPI.login import autoLogin

# from stock_API.deashinAPI.chartData import *


# import win32com.client

# actorcritic = ActorCritic()

# actorcritic.simulation_at_one_point()

# autoLogin()
# save_chart_history_kospi_N(N_th=200, maxCount=202000)

# mysql = MySQL_command()

# kospi_Nth_lists = kospi_Top_N_from_database(N_th=500).to_numpy()
# kospi_Nth_lists_code = [row[1] for row in kospi_Nth_lists]
# kospi_Nth_lists_code = kospi_Nth_lists_code[200:]
# save_chart_history_to_database(kospi_Nth_lists_code, maxCount=203000)


# delete_chart_by_date(20210527, code_idx_list=range(302, 501))

import platform

print(platform.architecture())
