import os
import pandas as pd
import numpy as np

from functions import map_columns, calc_and_group_durations, add_emissions

scenarios = ['25 GW (SC)', '25 GW (CC)', '35 GW', '55 GW']
savedir = 'results/Emissions/'
total = pd.DataFrame()

for s in scenarios:
    df = map_columns(s)
    grouped_df = calc_and_group_durations(s, df)
    e_df = add_emissions(grouped_df)
    l = len(e_df)
    s_name = [s] * l
    e_df['Scenario'] = s_name

    savepath = savedir + s + '_emissions.xlsx'
    e_df.to_excel(savepath)

    total = pd.concat([total, e_df])

total.set_index('Scenario', drop=True, inplace=True)
t_save = savedir + 'all_scenarios.xlsx'
total.to_excel(t_save)
