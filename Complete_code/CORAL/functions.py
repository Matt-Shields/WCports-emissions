import os
import pandas as pd
import numpy as np

def map_columns(scenario):
    """
    - Map CORAL vessel types (agents) to vessels for which emissions factors are available;
    - Map CORAL activities to transit, maneuvering, idling at sea, idling at port;
    - Specify number of vessels for each group (1 for all except towing groups);
    - Specify multiplier for calculating engine on hours (engines are assumed to be on for
      100% of activity duration except for delays, during which engines are assumed to
      be on for only 25% of duration).
    """
    filename = "Action_logs_for_emissions/" + scenario + "_agent_actions_sum.csv"

    df = pd.read_csv(filename)

    vessels = {
        "Array Cable Installation Vessel": "CLV",
        "Export Cable Installation Vessel": "CLV",
        "Floating Substation Installation Vessel": "AHTS",
        "Mooring System Installation Vessel": "AHTS",
        "Onshore Construction": "Onshore",
        "Substation Assembly Line 1": "HLV",
        "Substructure Assembly Line 1": "HLV",
        'Towing Group 1': "Towing Group",
        "Towing Group 2": "Towing Group",
        "Towing Group 3": "Towing Group",
        "Turbine Assembly Line 1": "HLV"
    }

    actions = {
        "Attach Topside": "Idle at port",
        "Ballast to Operational Draft": "Idle at port",
        "Ballast to Towing Draft": "Idle at port",
        "Check Mooring Lines": "Idle at sea",
        "Connect Mooring Lines": "Idle at sea",
        "Connect Mooring Lines, Pre-tension and pre-stretch": "Idle at sea",
        "Delay": "Idle at port",
        "Delay: No Completed Assemblies Available": "Idle at port",
        "Delay: No Substructures in Wet Storage": "Idle at port",
        "Delay: Waiting on Completed Assembly": "Idle at port",
        "Electrical Completion": "Idle at port",
        "Install Drag Embedment Anchor": "Idle at sea",
        "Install Mooring Lines": "Idle at sea",
        "Install Suction Pile Anchor": "Idle at sea",
        "Lay/Bury Cable": "Transit",
        "Lift and Attach Blade": "Idle at port",
        "Lift and Attach Nacelle": "Idle at port",
        "Lift and Attach Tower Section": "Idle at port",
        "Load Cable": "Idle at port",
        "Load Mooring System": "Idle at port",
        "Lower Cable": "Idle at sea",
        "Mechanical Completion": "Idle at port",
        "Mobilize": "Idle at port",
        "Move Substructure": "Transit",
        "Onshore Construction": "Idle at port",
        "Perform Mooring Site Survey": "Idle at sea",
        "Position Onsite": "Maneuvering",
        "Position Substructure": "Maneuvering",
        "Prepare Cable": "Idle at port",
        "Prepare for Turbine Assembly": "Idle at port",
        "Prepare Cable": "Idle at port",
        "Prepare for Turbine Assembly": "Idle at port",
        "Pull in Cable": "Idle at port",
        "Pull Winch": "Idle at sea",
        "Raise Cable": "Idle at sea",
        "Splice Cable": "Idle at sea",
        "Substation Substructure Assembly": "Idle at port",
        "Substructure Assembly": "Idle at port",
        "Terminate Cable": "Idle at port",
        "Tow Plow": "Transit",
        "Tow Substation to Site": "Transit",
        "Tow Substructure": "Transit",
        "Transit": "Transit"
    }

    num_vessels = {
        "Array Cable Installation Vessel": 1,
        "Export Cable Installation Vessel": 1,
        "Floating Substation Installation Vessel": 1,
        "Mooring System Installation Vessel": 1,
        "Onshore Construction": 0,
        "Substation Assembly Line 1": 1,
        "Substation Assembly Line 2": 1,
        "Substructure Assembly Line 1": 1,
        "Substructure Assembly Line 2": 1,
        "Towing Group 1": 3,
        "Towing Group 2": 3,
        "Towing Group 3": 3,
        "Turbine Assembly Line 1": 1,
        "Turbine Assembly Line 2": 1
    }

    engine_prop = {
        "Attach Topside": 1,
        "Ballast to Operational Draft": 1,
        "Ballast to Towing Draft": 1,
        "Check Mooring Lines": 1,
        "Connect Mooring Lines": 1,
        "Connect Mooring Lines, Pre-tension and pre-stretch": 1,
        "Delay": 0.25,
        "Delay: No Completed Assemblies Available": 0.25,
        "Delay: No Substructures in Wet Storage": 0.25,
        "Delay: Waiting on Completed Assembly": 0.25,
        "Electrical Completion": 1,
        "Install Drag Embedment Anchor": 1,
        "Install Mooring Lines": 1,
        "Install Suction Pile Anchor": 1,
        "Lay/Bury Cable": 1,
        "Lift and Attach Blade": 1,
        "Lift and Attach Nacelle": 1,
        "Lift and Attach Tower Section": 1,
        "Load Cable": 1,
        "Load Mooring System": 1,
        "Lower Cable": 1,
        "Mechanical Completion": 1,
        "Mobilize": 1,
        "Move Substructure": 1,
        "Onshore Construction": 1,
        "Perform Mooring Site Survey": 1,
        "Position Onsite": 1,
        "Position Substructure": 1,
        "Prepare Cable": 1,
        "Prepare for Turbine Assembly": 1,
        "Prepare Cable": 1,
        "Prepare for Turbine Assembly": 1,
        "Pull in Cable": 1,
        "Pull Winch": 1,
        "Raise Cable": 1,
        "Splice Cable": 1,
        "Substation Substructure Assembly": 1,
        "Substructure Assembly": 1,
        "Terminate Cable": 1,
        "Tow Plow": 1,
        "Tow Substation to Site": 1,
        "Tow Substructure": 1,
        "Transit": 1
    }

    df['Corresponding_vessels'] = df['agent'].map(vessels)
    df['Corresponding_actions'] = df['action'].map(actions)
    df['Number_of_vessels'] = df['agent'].map(num_vessels)
    df['Engine_on_proportion'] = df['action'].map(engine_prop)

    return df

def calc_and_group_durations(scenario, df):
    """
    - Calculate engine on hours based on activity durations and multipliers;
    - Group action logs by vessels and activities, summing engine on hours for each.
    """
    savepath = "results/Full_Dataframes/" + scenario + '_full_df.csv'

    df['Engine_on_hours'] = df.duration * df.Number_of_vessels * df.Engine_on_proportion
    df_grouped = df.groupby(['Corresponding_vessels', 'Corresponding_actions']).sum(numeric_only=True)['Engine_on_hours']

    df_grouped.to_csv(savepath)
    new_df = pd.read_csv(savepath)

    return new_df

def add_emissions(df):
    """
    - Map emissions factors to corresponding vessels and actions;
    - Multiply engine on hours by associated emissions factors to calculate total emissions.
    """
    efs = {
        ('SPV', 'Transit'): 4.1486896752,
        ('SPV', 'Maneuvering'): 3.9358741128,
        ('SPV', 'Idle at port'): 0.4444144376,
        ('SPV', 'Idle at sea'): 0.2222072188,
        ('AHTS', 'Transit'): 11.48620032,
        ('AHTS', 'Maneuvering'): 6.93707868,
        ('AHTS', 'Idle at port'): 1.16877936,
        ('AHTS', 'Idle at sea'): 0.58438968,
        ('CTV', 'Transit'): 1.111751032,
        ('CTV', 'Maneuvering'): 0.432559932,
        ('CTV', 'Idle at port'): 0.00695702,
        ('CTV', 'Idle at sea'): 0.00347851,
        ('FB', 'Transit'): 4.56130444,
        ('FB', 'Maneuvering'): 4.58220756,
        ('FB', 'Idle at port'): 0.804231512,
        ('FB', 'Idle at sea'): 0.47307736,
        ('SOV', 'Transit'): 4.501852376,
        ('SOV', 'Maneuvering'): 3.369358524,
        ('SOV', 'Idle at port'): 0.747183948,
        ('SOV', 'Idle at sea'): 0.373591974,
        ('CLV', 'Transit'): 4.1486896752,
        ('CLV', 'Maneuvering'): 2.5556911128,
        ('CLV', 'Idle at port'): 0.4444144376,
        ('CLV', 'Idle at sea'): 0.2222072188,
        ('HLV', 'Transit'): 14.875224448,
        ('HLV', 'Maneuvering'): 20.420014272,
        ('HLV', 'Idle at port'): 4.808692224,
        ('HLV', 'Idle at sea'): 2.404346112,
        ('WTIV', 'Transit'): 16.347419648,
        ('WTIV', 'Maneuvering'): 19.138415772,
        ('WTIV', 'Idle at port'): 4.808692224,
        ('WTIV', 'Idle at sea'): 2.404346112,
        ('OGV', 'Transit'): 2.08210464,
        ('OGV', 'Maneuvering'): 0.69403488,
        ('OGV', 'Idle at port'): 0.0,
        ('OGV', 'Idle at sea'): 0.0,
        ('Tug', 'Transit'): 1.3865398568,
        ('Tug', 'Maneuvering'): 0.5797480332,
        ('Tug', 'Idle at port'): 0.0265758164,
        ('Tug', 'Idle at sea'): 0.0132879082,
        ('Towing Group', 'Transit'): 4.753093345,
        ('Towing Group', 'Maneuvering'): 2.698858249,
        ('Towing Group', 'Idle at port'): 0.407310331,
        ('Towing Group', 'Idle at sea'): 0.203655165
    }

    df['Emissions_factor'] = df[['Corresponding_vessels', 'Corresponding_actions']].apply(tuple, axis=1).map(efs)

    df['Emissions_tons'] = df.Engine_on_hours * df.Emissions_factor

    return df
