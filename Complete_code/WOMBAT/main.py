import os
import pandas as pd
import numpy as np

from functions import get_data, group_activities, calc_emissions, efs, add_missing_vessels, join_dfs

output_file = 'WCports_results_23Mar.xlsx'
scenarios = ['WCports_test_ctv6', 'WCports_test_ctv8', 'WCports_test_sov6']

savedir = 'results/emissions/'

## percent of transit time to bin as maneuvering
perc_m = 0.1
## proportion of 'idling at port' hours with engine on
perc_ip = 0.25

dfs = []
ports_headers = []

for s in scenarios:
    times_df = get_data(s, output_file)
    grouped_df, ports = group_activities(times_df, perc_m, perc_ip)
    ports_headers += ports
    emissions_df = calc_emissions(grouped_df, efs, ports)
    dfs.append(emissions_df)

dfs_list = add_missing_vessels(dfs, ports_headers)
all_emissions = join_dfs(dfs_list, savedir)
