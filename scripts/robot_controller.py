#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry # Import the message type needed for position
from geometry_msgs.msg import Twist # Import the message type needed for velocities
from assignment1_solution.srv import goal, goalResponse # Import custom service
from assignment1_solution.srv import hints, hintsResponse # Import custom service
import math # Needed for pi and cos
from time import sleep

vel_pub = rospy.Publisher('/cmd_vel',Twist,queue_size=1000) # Define the node as a publisher on the topic                                     # /cmd_vel with a message of 
                                # type geometry_msgs/Twist

client = rospy.ServiceProxy('/goal_generator', goal) #Define the node as a client for the service
                             #goal_generator with the custom service goal
                             
client2 = rospy.ServiceProxy('/hints_generator', hints) #Define the node as a client for the service
                             #hints_generator with the custom service hints

global who, what, where
global success
who = []
what = []
where = []

def velocity(x, y, t, tx, ty): # Velocity function takes as arguments:
                   # x  = the distance in x
                   # y  = the distance in y
                   # t  = the starting time
                   # tx = period of function vx
                   # ty = period of function vy

    #print("Computing velocities")

    now = rospy.get_time() # Get the time now and store it in the variable "now"

    #print(now-t)
 
    #print("Period of x is : %f" %(tx))
    #print("Period of y is : %f" %(ty))

    vel_msg = Twist() # vel_msg is defined as a message of type Twist()

    if((now-t)/(tx)>1): # Check if we are inside the period of function vx

        vx = 0 # The velocity should be null if 1 period has passed
    else:
        vx = ((x)/(abs(x))*0.5)*(1 - math.cos(2*math.pi*(now-t)/(tx))) # Velocity function for x

    if((now-t)/(ty)>1): # Check if we are inside the period of function vy

        vy = 0 # The velocity should be null if 1 period has passed
    else:
        vy = ((y)/(abs(y))*0.5)*(1 - math.cos(2*math.pi*(now-t)/(ty))) # Velocity function for y

    vel_msg.linear.x = vx # Store the velocity vx inside vel_msg.linear.x
    vel_msg.linear.y = vy # Store the velocity vy inside vel_msg.linear.y

    vel_pub.publish(vel_msg) # Publish the velocities in the /cmd_vel topic

    #print("Velocities are x: %f, y: %f" %(vx, vy))
    
def ask_to_Oracle():
                
        position = rospy.wait_for_message("/odom", Odometry) # Wait for 1 message to be publish on topic /odom

        distance_x = 0 - position.pose.pose.position.x # Compute distances between the goal and the
        distance_y = 0 - position.pose.pose.position.y # current position of the robot
    

        period_x = abs(2*distance_x) # Since the velocities in x and y will be computed with specific 
        period_y = abs(2*distance_y) # law of motions, we need to compute periods for both
                     # which depend on the distance

    #print("Goal generated is x: %f, y: %f" %(resp.x, resp.y))     # Print informations about goal coordinates
    #print("Distances are x: %f, y: %f" %(distance_x, distance_y)) # and distances
        print("I have a consistent hypothesis! I'm going to the central hall to ask to the Oracle... please wait...\n") # and distances

        t = rospy.get_time() # Get the time and save it in the variable t

        while(((abs(distance_x))>0.05) or ((abs(distance_y))>0.05)): # Robot should move until the distances from
                                     # goals go under 0.05

            velocity(distance_x, distance_y, t, period_x, period_y) # Execute function velocity
                                    # passing the distances,
                                    # the time saved in t and the periods
            position = rospy.wait_for_message("/odom", Odometry) # Wait for 1 message to be publish on 
                                     #topic /odom

            distance_x = 0 - position.pose.pose.position.x # Update current distance in x
            distance_y = 0 - position.pose.pose.position.y # Update current distance in x
            
    
    
def control():

    class counter():
        def __init__(self):
            self.what = 0
            self.who = 0
            self.where = 0
    ID_list = [counter() for i in range(1,8)]
    
    rospy.init_node('robot_controller') # Initialize the node with the name robot_controller

    rate = rospy.Rate(100) # Rate of the spinning loop will be 100hz
    
    success = 0

    while not success:
    
            
        resp = client(1) # Calls for service goal_generator giving 1 as bool request, the server will respond
         # generating a random goal and giving x and y coordinates to be reached
         
        
        position = rospy.wait_for_message("/odom", Odometry) # Wait for 1 message to be publish on topic /odom

        distance_x = resp.x - position.pose.pose.position.x # Compute distances between the goal and the
        distance_y = resp.y - position.pose.pose.position.y # current position of the robot
    

        period_x = abs(2*distance_x) # Since the velocities in x and y will be computed with specific 
        period_y = abs(2*distance_y) # law of motions, we need to compute periods for both
                     # which depend on the distance

    #print("Goal generated is x: %f, y: %f" %(resp.x, resp.y))     # Print informations about goal coordinates
    #print("Distances are x: %f, y: %f" %(distance_x, distance_y)) # and distances
        print("Going to a room... please wait...\n") # and distances

        t = rospy.get_time() # Get the time and save it in the variable t

        while(((abs(distance_x))>0.05) or ((abs(distance_y))>0.05)): # Robot should move until the distances from
                                     # goals go under 0.05

            velocity(distance_x, distance_y, t, period_x, period_y) # Execute function velocity
                                    # passing the distances,
                                    # the time saved in t and the periods
            position = rospy.wait_for_message("/odom", Odometry) # Wait for 1 message to be publish on 
                                     #topic /odom

            distance_x = resp.x - position.pose.pose.position.x # Update current distance in x
            distance_y = resp.y - position.pose.pose.position.y # Update current distance in x
            
        resp2 = client2(1)
        
        #print("Distances are x: %f, y: %f" %(distance_x, distance_y)) # Print current distances

    #print("Goal reached") # When the distances go under 0.05 than we exit from the while loop
                  # so we can print "goal reached" and the final position acquired

    #print("Position is x: %f, y: %f" %(position.pose.pose.position.x, position.pose.pose.position.y))
    
        for i in range (1, 7):
            #print(i)
            ID = list("ID0")
            ID[2] = str(i)
            CurrentID = "".join(ID)
            currenthint = str(resp2.hint)
            if (resp2.hint.startswith(CurrentID, 0, 3)):

                if ("what" in resp2.hint):
                    ID_list[i].what +=1
                    what.insert(i, currenthint[11:])
                    print(" I found what for ID number", str(i))
                if ("who" in resp2.hint):
                    ID_list[i].who +=1
                    who.insert(i, currenthint[10:])
                    print(" I found who for ID number", str(i))
                if ("where" in resp2.hint):
                    ID_list[i].where +=1
                    where.insert(i, currenthint[12:])
                    print(" I found where for ID number", str(i))                    
                
                if( ID_list[i].what == ID_list[i].who == ID_list[i].where == 1):
                    ask_to_Oracle()
                    correct_hypothesis = rospy.get_param('correct_HP0')
                    if ( correct_hypothesis == i ):
                        print("I GUESSED RIGHT!")
                        success = 1
                        print("The correct Hypothesis is ID", correct_hypothesis)
                        print(who[i], "with the", what[i], "in the", where[i])
                        sleep(3)                    
                    else:
                        print("I GUESSED WRONG!")
                        sleep(3)
                        continue
                    
                    
    
        #print(" ----------------------------------------")
        #print("| I found this hint: %s |" %(resp2.hint))
        #print(" ----------------------------------------")
        #print("\n")
        #print("I'm going to continue searching!")
        #print("\n")

    
if __name__ == '__main__':
    try:
        control() # Execute function control()
    except rospy.ROSInterruptException: # Keep going until keyboard exception (Ctrl+C)
        pass
