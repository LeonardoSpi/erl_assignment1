#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry # Import the message type needed for position
from geometry_msgs.msg import Twist # Import the message type needed for velocities
from assignment1_solution.srv import goal, goalResponse # Import custom service
from assignment1_solution.srv import hints, hintsResponse # Import custom service
import math # Needed for pi and cos
from time import sleep

vel_pub = rospy.Publisher('/cmd_vel',Twist,queue_size=1000) # Define the node as a publisher on the topic                                    
							     # /cmd_vel with a message of 
                                                            # type geometry_msgs/Twist

client = rospy.ServiceProxy('/goal_generator', goal) #Define the node as a client for the service
                             #goal_generator with the custom service goal
                             
client2 = rospy.ServiceProxy('/hints_generator', hints) #Define the node as a client for the service
                             #hints_generator with the custom service hints

global who, what, where # Initiate global variables
global success
who = []   # Define the global variable as a list
what = []  # Define the global variable as a list
where = [] # Define the global variable as a list

def velocity(x, y, t, tx, ty): # Velocity function takes as arguments:
                   # x  = the distance in x
                   # y  = the distance in y
                   # t  = the starting time
                   # tx = period of function vx
                   # ty = period of function vy


    now = rospy.get_time() # Get the time now and store it in the variable "now"

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

    
def ask_to_Oracle(): # Go to the Oracle
                
        position = rospy.wait_for_message("/odom", Odometry) # Wait for 1 message to be publish on topic /odom

        distance_x = 0 - position.pose.pose.position.x # Compute distances between the goal and the
        distance_y = 0 - position.pose.pose.position.y # current position of the robot
    

        period_x = abs(2*distance_x) # Since the velocities in x and y will be computed with specific 
        period_y = abs(2*distance_y) # law of motions, we need to compute periods for both
                     		      # which depend on the distance

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

    class counter():		# Define a class that contains three elements: what, who, where
        def __init__(self):	 
            self.what = 0	# These elements are needed as counters
            self.who = 0	# for each ID we will store how many source of information
            self.where = 0	# we found and most importantly of which type
            
    ID_list = [counter() for i in range(1,8)] 	# Create a list of objects of the class counter()
    
    rospy.init_node('robot_controller') # Initialize the node with the name robot_controller

    rate = rospy.Rate(100) # Rate of the spinning loop will be 100hz
    
    success = 0 # success is true only when the correct hypothesis is brought to the Oracle (Parameter_server)

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
            
        resp2 = client2(1) # Calls for service hints_generator giving 1 as bool request, the server will respond
        		   # with a string containing an ID as prefix separated by a comma, where/who/what separated by a comma, and the actual hint.
    
        for i in range (1, 7): # Cycle in the range of the IDs
            ID = list("ID0") 	# Create a list with the element 'I' 'D' '0'
            ID[2] = str(i)	# Replace the element '0' with the number i converted in a string
            CurrentID = "".join(ID) # Join the list ID in order to have a string
            currenthint = str(resp2.hint) # Store the hint found in the variable currenthint
            
            if (resp2.hint.startswith(CurrentID, 0, 3)): # Check whether the hint found has in the prefix the currentID,
            						  # when they match we will the variable i that correspond
            						  # to the ID of the hint we just found

                if ("what" in resp2.hint): # Check whether we found an hint of type what
                    ID_list[i].what +=1 # Update the counter of the object ID_list[i]
                    what.insert(i, currenthint[11:]) # Store the actual hint at the index i of the global list what, so that we can retrieve it later
                    print(" I found what for ID number", str(i))
                if ("who" in resp2.hint): # Check whether we found an hint of type who
                    ID_list[i].who +=1 # Update the counter of the object ID_list[i]
                    who.insert(i, currenthint[10:]) #Store the actual hint at the index i of the global list who, so that we can retrieve it later
                    print(" I found who for ID number", str(i))
                if ("where" in resp2.hint): # Check whether we found an hint of type where
                    ID_list[i].where +=1 # Update the counter of the object ID_list[i]
                    where.insert(i, currenthint[12:]) # Store the actual hint at the index i of the global list where, so that we can retrieve it later
                    print(" I found where for ID number", str(i))                    
                
                if( ID_list[i].what == ID_list[i].who == ID_list[i].where == 1): # If all the counters of this ID_list are 1, it means we found a consistent hypothesis
                    ask_to_Oracle() # Call the function ask_to_Oracle() which brings the robot to the default position x=0, y=0. This is where the Oracle is supposed to be
                    correct_hypothesis = rospy.get_param('correct_HP0') # Retrieve the correct hypothesis ID from the Oracle (parameter server)
                    if ( correct_hypothesis == i ): # Check if the hypothesis is not only consistent but also true
                        print("I GUESSED RIGHT!")
                        success = 1
                        print("The correct Hypothesis is ID", correct_hypothesis)
                        print(who[i], "with the", what[i], "in the", where[i]) # The robot guessed right so print the correct hypothesis in a statement
                        sleep(3)                    
                    else:
                        print("I GUESSED WRONG!")
                        sleep(3)
                        continue # The robot guessed wrong, continue cycling
                    
                    
    
        print(" ----------------------------------------")
        print("|        %s         |" %(resp2.hint)) # Print the hint found
        print(" ----------------------------------------")
        print("\n")

    
if __name__ == '__main__':
    try:
        control() # Execute function control()
    except rospy.ROSInterruptException: # Keep going until keyboard exception (Ctrl+C)
        pass
