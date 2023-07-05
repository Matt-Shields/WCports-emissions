
Calculate total emissions from all scenarios run in CORAL.

Instructions:
- Copy action logs from CORAL output:
  'CORAL/analysis/results/Actions/Action_logs_for_emissions'
- Run main.py

Areas that can be modified:
- L.18-30: Mapping of CORAL agents (vessels) to vessels for which we have
  emissions factors.
- L.32-76: Mapping of CORAL activities to transit, maneuvering, idling at
  port, and idling at sea. Update this if new activities or delays are
  added to CORAL.
- L.78-93: Number of individual vessels in each vessel type (1 for all
  vessel types except for towing groups).
- L.95-139: Assign multiplier for the proportion of time that engine is on
  for each activity (engines are assumed to be on for 100% of the activity
  duration for all activities besides delays, for which engines are assumed
  to be on for 25% of the duration).
- L.168-213: Map emissions factors to corresponding vessels and activities.
  Adjust this if emissions factors change.

Vessels mapping: CORAL agent name -> Vessel
- Array Cable Installation Vessel -> CLV
- Export Cable Installation Vessel -> CLV
- Floating Substation Installation Vessel -> AHTS
- Mooring System Installation Vessel -> AHTS
- Onshore Construction -> Onshore
- Substation Assembly Line 1 -> HLV
- Substructure Assembly Line 1 -> HLV
- Towing Group 1 -> Towing Group (1 AHTS + 2 tugs)
- Towing Group 2 -> Towing Group (1 AHTS + 2 tugs)
- Towing Group 3 -> Towing Group (1 AHTS + 2 tugs)
- Turbine Assembly Line 1 -> HLV
