# ROS_NMEA_Echosounder
ROS nodes for an NMEA Echosounder


Echosounder_temperature.py reads data from an NMEA Echosounder.

Lines starting with $SDMTW contain water temperature.
Lines starting with $SDDPT contain depth, calculated with a value of 1500m/s for speed of sound in the case of Airmar echosounders.

This node reads the data and recalculates depth taking into account water temperature, depth and a salinity value that you can edit depending on whether you are operating in freshwater or seawater.
