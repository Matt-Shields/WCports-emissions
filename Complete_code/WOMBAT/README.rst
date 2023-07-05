
Use WOMBAT output files to calculate emissions from
CTV and SOV scenarios

NOTE: calculated values are for one project and one year. For
total scenario emissions, each port serves 3 projects for 20 years.

Potential changes for future runs:
  main.py
    - L.7: output file name
    - L.8: list of CTV and SOV scenario names
  functions.py
    - L.74: this line extracts only the rows showing vessel hours
      from the output file. Check the number in 'tail()' if other output
      is changed.
    - L.5-30: edit emissions factors if any vessel types are added
      (copy & paste numbers from emissions-factors.xlsx). If needed,
      can also add weighted towing group emissions factors.

Final output is the 'results/Emissions/total_emissions.xlsx' file, which
shows emissions for each vessel type, activity, and associated port.
Emissions are disaggregated across ports to make them easier to map to
the low/medium/high O&M scenarios.

To calculate scenario emissions, copy/paste 'total_emissions.xlsx' into
the O&M sheet of the scenario-mapping.xlsx spreadsheet in Teams.
