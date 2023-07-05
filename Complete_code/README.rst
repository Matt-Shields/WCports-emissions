Instructions for emissions calculations:

- For installation emissions:
  - After running CORAL, duplicate the results > Actions > Action_logs_for_emissions
  - Put that folder into the directory containing the emissions post processing script.
  - Run 'main.py' in the CORAL folder.
  - Main output is results/Emissions/all_scenarios.xlsx

- For O&M emissions:
  - After running CORAL, put all output files into separate tabs of an excel file.
  - Move that excel file to the directory containing the emissions post processing script.
  - Run 'main.py' in the WOMBAT folder.
  - Main output is results/Emissions/total_emissions.csv

- Use the 'scenarios_template.xlsx' spreadsheet (in Teams) to map
  emissions to scenarios in ports assessment.
  - Copy 'CORAL/reuslts/Emissions/all_scenarios.xlsx' into
    the 'CORAL-emissions' sheet, in cell A10.
      - This is easy if you're running all phases (including cable
        and mooring installation).
      - This is a little tedious if you're not running all phases, as
        some vessel types won't be used. All vessel types need to stay in
        the correct rows for accurate results.
  - Copy 'WOMBAT/results/Emissions/total_emissions.csv' into
    the 'WOMBAT-emissions' sheet, in cell A10.

- The template will map emissions results from different
  installation and O&M strategies to the defined port scenarios.
  The spreadsheet will have to be adjusted if any of the following
  are changed:
  - Ports to be used in the low, medium, or high O&M scenarios, and
    whether they use the CTV or SOV strategy.
  - How many projects an O&M port can serve simultaneously (currently 3).
  - FOSW project lifetime (currently 20 years).
  - Emissions factors (calculated in the 'vessel-emissions.xlsx' spreadsheet,
    and copied into 'emissions-factor.xlsx').
  - Capacity factor of projects (currently 0.46).
  - Distances between ports and MF sites.
