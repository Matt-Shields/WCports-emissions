import matplotlib.cm as cm
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.text as txt
import matplotlib.patches as mpatches
from matplotlib.patches import Patch
import os
import datetime as dt
import pandas as pd
import numpy as np

def plot_emissions(sn, df_name):

    df = pd.read_excel(df_name, sheet_name = sn)

    x_ind = np.arange(0, 10, 1)

    fig = plt.figure(figsize=(9, 6))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    width = 0.4

    inst_int = np.array(df['Installation intensity'])
    om_int = np.array(df['O&M intensity'])
    ct_int = np.array(df['CT intensity'])

    inst_abs = np.array(df['Installation absolute']/1000000)
    om_abs = np.array(df['O&M absolute']/1000000)
    ct_abs = np.array(df['CT absolute']/1000000)

    ax1.bar(x_ind-(width/2), inst_int, color='#117864', width=width)
    ax1.bar(x_ind-(width/2), om_int, bottom=inst_int, color='#1ABC9C', width=width)
    ax1.bar(x_ind-(width/2), ct_int, bottom=om_int+inst_int, color='#A3E4D7', width=width)

    ax2.bar(x_ind+(width/2), inst_abs, color='#9C640C', width=width)
    ax2.bar(x_ind+(width/2), om_abs, bottom=inst_abs, color='#F39C12', width=width)
    ax2.bar(x_ind+(width/2), ct_abs, bottom=om_abs+inst_abs, color='#FAD7A0', width=width)

    ax1.set_ylim([0,33])
    ax2.set_ylim([0,100])

    ax1.set_ylabel('Carbon intensity (g CO2/kWh)', weight='bold')
    ax2.set_ylabel('Absolute lifetime emissions (million metric tons CO2)', weight='bold')

    ax1.set_title('Total emissions across all phases', weight='bold')

    ax1.set_xlabel('Scenario', weight='bold')
    ax1.set_xticks(x_ind)
    ax1.set_xticklabels(df['Scenario name'], rotation=45)

    handles = [
        Patch(facecolor=color, label=label)
        for label, color in zip(['Intensity: installation', 'Intensity: O&M', 'Intensity: Component transportation', 'Emissions: Installation', 'Emissions: O&M', 'Emissions: Component transportation'], ['#117864', '#1ABC9C', '#A3E4D7', '#9C640C', '#F39C12', '#FAD7A0'])
        ]

    ax1.legend(handles=handles, loc='upper left')

    fname = 'Figures/all-emissions.png'
    fig.savefig(fname, bbox_inches='tight', dpi=300)

def activity_plot(sn, df_name):
    df = pd.read_excel(df_name, sheet_name = sn)
    activities = ['Transit', 'Maneuvering', 'Idle at port', 'Idle at sea']
    for a in activities:
        df[a] = df[a]/1000000

    ax = df.plot.bar(x = 'Scenario name', y = ['Transit', 'Maneuvering', 'Idle at sea', 'Idle at port'], color=['#C0392B', '#2980B9', '#FFC107', '#27AE60'], stacked = True, rot=0, title='Scenario-wide emissions by vessel activity')
    plt.ylabel('Million metric tons of CO2', weight='bold')
    plt.legend(loc = 'upper left')

    ax.set_xticklabels(df['Scenario name'], rotation=45)
    ax.set_title('Absolute emissions by activity', weight='bold')
    ax.set_xlabel('Scenario', weight='bold')

    savedir = 'Figures/'
    fig = ax.get_figure()
    savefig = savedir + 'emissions-by-activity.png'
    fig.savefig(savefig, bbox_inches='tight', dpi=300)

sn = 'summary_rename'
df_name = 'scenarios_template.xlsx'
plot_emissions(sn, df_name)
activity_plot(sn, df_name)
