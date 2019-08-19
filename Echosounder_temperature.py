\begin{lstlisting}[language=Python]
#!/usr/bin/python
import csv
import os, sys
import serial
import time
import roslib;
import sensor_msgs;
import rospy;
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from sensor_msgs.msg import TimeReference
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import TwistWithCovarianceStamped
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped
import tf2_ros
import tf2_geometry_msgs


pub = rospy.Publisher('/sonarpose', PoseStamped, queue_size=10)
rospy.init_node('talker', anonymous=True)
ser = serial.Serial('/dev/Echosounder',4800, timeout =2)
sound_velocity=1500#starting value
S=0#this is the salinity
D=0.5#starting value depth of echosounder
while True:
   line = ser.readline() # read the echosounder data
   if len(line) == 0: # in case it's switched off
      sys.exit()
   if "$SDDPT" in line: #this line contains depth calculated using default speed of sound
      Timestamp=rospy.Time.now()
      Timestamp_corrected=rospy.Time()
      Timestamp_corrected.secs=Timestamp.secs
      Timestamp_corrected.nsecs=Timestamp.nsecs-1000000 #This allows you to correct for latency
      listofchars=line.split(',')
      try:
         echorange=float((listofchars[1]))
         echosounder_time_of_travel=echorange/1500 #Airmar EchoRange SS510 uses 1500 as speed of sound
         echorange_salinity_temp_corrected=sound_velocity*echosounder_time_of_travel
         D=echorange_salinity_temp_corrected/2 #speed of sound varies with pressure, i e depth. This is an approximation
         pos=PoseStamped() # echosounder range in the reference frame of the echosounder
         pos.header.seq=1
         pos.header.stamp = Timestamp_corrected
         pos.header.frame_id = 'sonar'
         pos.pose.position.z=-1*echorange_salinity_temp_corrected
         pub.publish(pos)
      except:
         print("wait for it") 
   if "$SDMTW" in line: #this line contains water temperature
      listofchars_temp=line.split(',')
      try:
         T=float((listofchars_temp[1]))
        # Mackenzie equation below:
         sound_velocity=1448.96 + 4.591*T - (5.304*10**-2)*T**2 + (2.374*10**-4)*T**3 + 1.340*(S-35) + (1.630*10-2)*D + (1.675 *10**-7)*D**2 - (1.025*10**-2)*T*(S-35)- (7.139*10**-13)*T*D**3
      except:
         print("wait for it")
