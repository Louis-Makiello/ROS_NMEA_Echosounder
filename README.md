# ROS_NMEA_Echosounder
ROS nodes for an NMEA Echosounder

Echosounder_temperature.py reads data from an NMEA Echosounder.

Lines starting with $SDMTW contain water temperature.
Lines starting with $SDDPT contain depth, calculated with a value of 1500m/s for speed of sound in the case of Airmar echosounders.

This node reads the data and recalculates depth taking into account water temperature, depth and a salinity value that you can edit depending on whether you are operating in freshwater or seawater. It uses the Mackenzie equation for speed of sound in water.


Sonar_utm_transform.py transforms Echosounder range into x,y,z coordinates in the UTM world frame. It also publishes a marker of the echosounder's echo so that it can be vizualised in Rviz. The size of the marker reflect the size of the ensonified area. The colour of the marker reflects the depth of the water.

For it to work, it needs tf messages containing a transformation of the echosounder head's location to the UTM frame (this can be done with a GPS and an IMU).

Go to https://lowcosthydrography.wordpress.com/ to see these nodes in action.
