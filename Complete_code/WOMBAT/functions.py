import os
import pandas as pd
import numpy as np

## emissions factor for vessel types and activities
efs = {
    ('aht', 'transit'): 11.48620032,
    ('aht', 'maneuvering'): 6.93707868,
    ('aht', 'idle at port'): 1.16877936,
    ('aht', 'idle at site'): 0.58438968,
    ('clv', 'transit'): 4.148689675,
    ('clv', 'maneuvering'): 2.555691113,
    ('clv', 'idle at port'): 0.444414438,
    ('clv', 'idle at site'): 0.222207219,
    ('dsv', 'transit'): 1.111751032,
    ('dsv', 'maneuvering'): 0.432559932,
    ('dsv', 'idle at port'): 0.00695702,
    ('dsv', 'idle at site'): 0.00347851,
    ('ctv', 'transit'): 1.111751032,
    ('ctv', 'maneuvering'): 0.432559932,
    ('ctv', 'idle at port'): 0.00695702,
    ('ctv', 'idle at site'): 0.00347851,
    ('sov', 'transit'): 4.501852376,
    ('sov', 'maneuvering'): 3.369358524,
    ('sov', 'idle at port'): 0.747183948,
    ('sov', 'idle at site'): 0.373591974,
    ('tug', 'transit'): 11.48620032,
    ('tug', 'maneuvering'): 6.93707868,
    ('tug', 'idle at port'): 1.16877936,
    ('tug', 'idle at site'): 0.58438968
}


def get_data(s, output_file):
    """
    - Read WOMBAT output files for individual SOV or CTV runs,
      and extract only the rows containing activity durations.
    - Designate vessel types and activities in separate columns.
    - Return dataframe for each scenario showing duration for each
      vessel type, WOMBAT activity (not including maneuvering), and
      associated port.
    """

    av_map = {
    'aht idle at port': 'aht idle at port',
    'aht transit time': 'aht transit',
    'aht idle at sea': 'aht idle at site',
    'dsv idle at port': 'dsv idle at port',
    'dsv transit time': 'dsv transit',
    'dsv idle at sea': 'dsv idle at site',
    'tug 1 idle at port': 'tug idle at port',
    'tug 1 transit time': 'tug transit',
    'tug 1 idle at sea': 'tug idle at site',
    'tug 2 idle at port': 'tug idle at port',
    'tug 2 transit time': 'tug transit',
    'tug 2 idle at sea': 'tug idle at site',
    'ctv 1 idle at port': 'ctv idle at port',
    'ctv 1 transit time': 'ctv transit',
    'ctv 1 idle at sea': 'ctv idle at site',
    'ctv 2 idle at port': 'ctv idle at port',
    'ctv 2 transit time': 'ctv transit',
    'ctv 2 idle at sea': 'ctv idle at site',
    'ctv 3 idle at port': 'ctv idle at port',
    'ctv 3 transit time': 'ctv transit',
    'ctv 3 idle at sea': 'ctv idle at site',
    'ctv 4 idle at port': 'ctv idle at port',
    'ctv 4 transit time': 'ctv transit',
    'ctv 4 idle at sea': 'ctv idle at site',
    'ctv 5 idle at port': 'ctv idle at port',
    'ctv 5 transit time': 'ctv transit',
    'ctv 5 idle at sea': 'ctv idle at site',
    'cable 1 idle at port': 'clv idle at port',
    'cable 1 transit time': 'clv transit',
    'cable 1 idle at sea': 'clv idle at site',
    'cable 2 idle at port': 'clv idle at port',
    'cable 2 transit time': 'clv transit',
    'cable 2 idle at sea': 'clv idle at site',
    'sov idle at port': 'sov idle at port',
    'sov transit time': 'sov transit',
    'sov idle at sea': 'sov idle at site'
    }

    df_raw = pd.read_excel(output_file, sheet_name=s)
    times_df = df_raw.tail(-28).reset_index(drop=True)

    mapping = {times_df.columns[0]: 'Vessels and activity', times_df.columns[1]: 'units'}
    times_df.rename(columns=mapping, inplace=True)

    times_df['Combined'] = times_df['Vessels and activity'].map(av_map)
    split = times_df['Combined'].str.split(" ", n=1, expand=True)
    times_df['Vessel'] = split[0]
    times_df['Activity'] = split[1]
    times_df.drop(['Combined', 'Vessels and activity'], axis=1, inplace=True)

    return times_df

def group_activities(times_df, perc_m, perc_ip):
    """
    - Make a list of all port names in the given scenario.
    - Create separate dataframes for transit (1-perc_m % of WOMBAT's)
      transit duration), maneuvering (perc_m % of WOMBAT's transit
      duration), idling at port, and idling at site. Concatenate
      these four dataframes together.
    - Group dataframe by vessel and activity, summing activity durations.
    - Return dataframe showing all four activities, all vessel types, and
      associated ports. Also return list of ports in the present scenario.
    """

    string_cols = ['units', 'Vessel', 'Activity']
    ports = []
    for col in times_df:
        if col not in string_cols:
            ports.append(col)

    t_df = times_df[times_df.Activity == 'transit'].reset_index(drop=True)
    for col in t_df:
        if col in ports:
            t_df[col] = t_df[col].multiply((1-perc_m))

    m_df = times_df[times_df.Activity == 'transit'].reset_index(drop=True)
    for col in m_df:
        if col in ports:
            m_df[col] = m_df[col].multiply(perc_m)
    m_df['Activity'] = m_df['Activity'].replace('transit', 'maneuvering')

    ip_df = times_df[times_df.Activity == 'idle at port'].reset_index(drop=True)
    for col in ip_df:
        if col in ports:
            ip_df[col] = ip_df[col].multiply(perc_ip)

    is_df = times_df[times_df.Activity == 'idle at site'].reset_index(drop=True)

    new_df = pd.concat([t_df, m_df, ip_df, is_df]).reset_index(drop=True)

    df_grouped = new_df.groupby(['Vessel', 'Activity'], as_index=False).sum(numeric_only=True)

    return df_grouped, ports

def calc_emissions(df_grouped, efs, ports):
    """
    - If the present scenario includes Humboldt Bay, add a duplicate
      column (to account for doubled O&M capabilities at Humboldt).
    - Map emissions factors (tons CO2 / hour) to vessels and activities.
    - Create columns showing emissions associated with each port, then
      multiply durations by emissions factors to get total emissions
      (tons CO2) for each vessel and activity at each port.
    - Return a dataframe showing durations and emissions for each
      port, vessel, and activity.
    """

    if 'Humboldt' in ports:
        df_grouped['Humboldt 2'] = df_grouped['Humboldt']
        ports.append('Humboldt 2')
    if 'CrescentCity_H' in ports:
        df_grouped['Crescent_City_2'] = df_grouped['CrescentCity_H']
        ports.append('Crescent_City_2')

    df_grouped['Emissions_factor'] = df_grouped[['Vessel', 'Activity']].apply(tuple, axis=1).map(efs)

    emissions_cols = []
    for name in ports:
        col_head = name + ' emissions (tons)'
        emissions_cols.append(col_head)

    for port, ems in zip(ports, emissions_cols):
        df_grouped[ems] = df_grouped[port] * df_grouped['Emissions_factor']

    return df_grouped

def add_missing_vessels(dfs, ports_headers):
    """
    - For CTV scenarios, add empty rows with SOV vessels.
    - For SOV scenarios, add empty rows with CTV vessels.
    - Set vessels and activities as the indeces of each
      dataframe and order them alphabetically so they can
      be joined without jumbling the order.
    - Drop all columns showing durations and emissions
      factors, so that only absolute emissions remain.
    - Return dataframes showing only absolute emissions
      for each vessel, activity, and port. Includes empty
      rows for CTV or SOV vessels, so that all dataframes
      have identical indeces whether they represent a CTV or
      a SOV scenario.
    """

    adjusted = []
    activities = ['idle at port', 'idle at site', 'maneuvering', 'transit']

    for df in dfs:

        if 'ctv' in df.values:
            df_copy = pd.DataFrame().reindex_like(df.head(4))
            df_copy['Vessel'] = df_copy['Vessel'].fillna('sov')
            df_copy['Activity'] = activities
        elif 'sov' in df.values:
            df_copy = pd.DataFrame().reindex_like(df.head(4))
            df_copy['Vessel'] = df_copy['Vessel'].fillna('ctv')
            df_copy['Activity'] = activities

        df = pd.concat([df, df_copy], axis=0)
        df.set_index(['Vessel', 'Activity'], drop=True, inplace=True)
        df.fillna(0, inplace=True)
        df.sort_index(ascending=True, inplace=True)

        for col in df:
            if col in ports_headers:
                df.drop(col, axis=1, inplace=True)

        df.drop('Emissions_factor', axis=1, inplace=True)

        adjusted.append(df)

    return adjusted

def join_dfs(df_list, savedir):
    """
    - Join all dataframes together, and export to results/Emissions.
    """
    #joined_df = df_list[0].join(df_list[1:], lsuffix='_caller', rsuffix='_other')
    joined_df = df_list[0].join(df_list[1:])
    joined_df.drop('Humboldt 2', axis=1, inplace=True)
    joined_df.drop('Crescent_City_2', axis=1, inplace=True)

    filepath = savedir + 'total_emissions.csv'
    joined_df.to_csv(filepath)
