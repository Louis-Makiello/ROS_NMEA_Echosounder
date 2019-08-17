#!/usr/bin/env python  
import rospy

import math
import tf2_ros
import geometry_msgs.msg
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped
import tf2_ros
import tf2_geometry_msgs
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import csv

class Colour:
        def __init__(self,r,g,b,a):
                self.r=r
                self.g=g
                self.b=b
                self.a=a
Red=Colour(255,0,0,1)
Orange=Colour(255,128,0,1)
Yellow=Colour(255,255,0,1)
Green=Colour(0,255,0,1)
Blue=Colour(0,0,255,1)
Purple=Colour(51,0,102,1)

csvfile='/home/ubuntu/Desktop/Echo_locationPP.txt'
rospy.init_node('tf2_sonar_coordinates')
i=0
def callback(data):
        #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)
        pos=PoseStamped()
        pos.header.stamp = data.header.stamp
        pos.header.frame_id = data.header.frame_id
        pos.pose.position.x = data.pose.position.x
        pos.pose.position.y = data.pose.position.y
        pos.pose.position.z = data.pose.position.z
        pos.pose.orientation.x = data.pose.orientation.x
        pos.pose.orientation.y = data.pose.orientation.y
        pos.pose.orientation.z = data.pose.orientation.z
        pos.pose.orientation.w =data.pose.orientation.w
        tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
        tf_listener = tf2_ros.TransformListener(tf_buffer)
        transform = tf_buffer.lookup_transform( 'utm',pos.header.frame_id, #source frame
                                     rospy.Time(0), #get the tf at first available time
                                     rospy.Duration(1.0)) #wait for 1 second
        transformodom = tf_buffer.lookup_transform('odom',pos.header.frame_id, #source frame ('utm',pos.header.frame_id,
                                      rospy.Time(0), #get the tf at first available time
                                      rospy.Duration(1.0)) #wait for 1 second
        pose_transformed = tf2_geometry_msgs.do_transform_pose(pos, transform)
        pose_transformed_odom = tf2_geometry_msgs.do_transform_pose(pos, transformodom)       
        publisher_sonar.publish(pose_transformed)
        #print(pose_transformed)
        Sonar_echo = Marker()
        Sonar_echo_Array=MarkerArray()
        Sonar_echo.header.frame_id = 'odom'
        Sonar_echo.header.stamp = rospy.Time.now()
        Sonar_echo.type = Marker.CYLINDER
        Sonar_echo.pose.position.x = pose_transformed_odom.pose.position.x
        Sonar_echo.pose.position.y = pose_transformed_odom.pose.position.y
        Sonar_echo.pose.position.z = pose_transformed_odom.pose.position.z
        Sonar_echo.pose.orientation.x = 0
        Sonar_echo.pose.orientation.y = 0
        Sonar_echo.pose.orientation.z = 0
        Sonar_echo.pose.orientation.w = 1
            #Imu_vizualisation.scale.x = 1
        Sonar_echo.scale.x = 3*(math.tan(math.radians(4.5)))*abs(data.pose.position.z)#Make it three times the size of the real ensonified area. data.pose.position.z is the range of the echosounder(abs makes it positive)
        Sonar_echo.scale.y = Sonar_echo.scale.x
        Sonar_echo.scale.z = 0.1
        if Sonar_echo.pose.position.z>=-1:
                TheColour=Red
        if -1>Sonar_echo.pose.position.z>=-2:
                TheColour=Orange
        if -2>=Sonar_echo.pose.position.z>=-3:
                TheColour=Yellow
        if -3>=Sonar_echo.pose.position.z>=-4:
                TheColour=Green
        if -4>=Sonar_echo.pose.position.z>=-5:
                TheColour=Blue
        if -5>=Sonar_echo.pose.position.z:
                TheColour=Purple                
        Sonar_echo.color.a = TheColour.a
        Sonar_echo.color.r = TheColour.r
        Sonar_echo.color.g = TheColour.g
        Sonar_echo.color.b = TheColour.b
        global i
        Sonar_echo.id=i
        Sonar_echo_Array.markers.append(Sonar_echo)
        i+=1               
        Sonar_echo_publisher.publish(Sonar_echo_Array)
        x_echo=pose_transformed.pose.position.x
        y_echo=pose_transformed.pose.position.y
        z_echo=pose_transformed_odom.pose.position.z
        timestampS=rospy.Time.now()
        thedata=[x_echo,y_echo,z_echo,timestampS]
        with open( csvfile, "a") as output:
                writer=csv.writer(output, delimiter=',',lineterminator='\n')
                writer.writerow(thedata)

        


##print(pose_transformed)

def listener():
  

    rospy.Subscriber('/sonarpose', PoseStamped, callback)
    
publisher_sonar= rospy.Publisher('/sonar_coordinates', PoseStamped, queue_size=10)
Sonar_echo_publisher = rospy.Publisher("Sonar_echo_MarkerArray", MarkerArray,queue_size=10)

count = 0
listener()
rospy.spin()
