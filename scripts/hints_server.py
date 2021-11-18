#!/usr/bin/env python

import rospy
import random # This library is needed to computed random numbers
from numpy import random

from assignment1_solution.srv import hints, hintsResponse # Import custom service of type goal

global hints_list

		
hints_list = ['','','','','','','','','','','','','','','','','','','']

def create_random_hints():

	informations =[ ('who, Rev.Green'		),
		('who, Prof. Plum'		),
		('who, Col. Mustard'		),
		('who, Mrs. Peacock'		),
		('who, Miss. Scarlett'		),
		('who, Mrs. White'		),
		
		
		('what, Candestick'		),
		('what, Dagger'		),
		('what, Lead Pipe'		),
		('what, Revolver'		),
		('what, Rope'			),
		('what, Spanner'		),
		
		
		('where, Conservatory'		),
		('where, Lounge'		),
		('where, Kitchen'		),
		('where, Library'		),
		('where, HallConservatory'	),
		('where, Study'		),
		]

	n = 1
	index = 1
	while (n < 18):
		ID = list("ID0, ")
		ID[2] = str(index)
		CurrentID = "".join(ID)
		for i in range (0, 3):
			selection = random.choice(informations)
			hints_list[n+i] = CurrentID + (selection)
			informations.remove(selection)
			print(hints_list[n+i])
		n = n + 3
		index = index + 1	

	n = 1
	index = 1
	consistent = 0
	
	while (n<18):
		
		index = 1
			
		if ((("who" in hints_list[n])or("who" in hints_list[n+1])or("who" in hints_list[n+2]))and
		    (("what" in hints_list[n])or("what" in hints_list[n+1])or("what" in hints_list[n+2]))and
		    (("where" in hints_list[n])or("where" in hints_list[n+1])or("where" in hints_list[n+2]))):
	
			print("A consistent hint was generated")
			print(hints_list[n:n+3])
			consistent += 1
			rospy.set_param('/correct_HP0', (int((n+2)/3)))
			break
		else:
			print("This hypothesis is unconsistent")
			print(hints_list[n:n+3])
			if((n==16)and(consistent == 0)):
				create_random_hints()	
			
		n = n + 3	
		index = index + 1
	

def handle_hints_generator(req): # Callback of the service
	if(req.request is True): # The request sent by the client is a bool
				 # If it is True than the robot entered a room and must receive an hint
		
		if( len(hints_list) > 0):
			hint = random.choice(hints_list)
			hints_list.remove(hint)
		else:
			hint = 'No more hints! all have been found'
		
		return hintsResponse(hint) # Returns the hint generated

def hints_server():
	rospy.init_node('hints_server') # Initialize the node as goal_server
	s = rospy.Service('hints_generator', hints, handle_hints_generator) # The nodes works as a server for the
								 	# service hints_generator

	print("\n")
	print("Waiting for requests:") # Once the node is started, print to screen so that
					 # the user knows it is ready to generate a goal

	rospy.spin() # Continue to cycle

if __name__ == '__main__':
    try:
        create_random_hints()
    except rospy.ROSInterruptException: # Keep going until keyboard exception (Ctrl+C)
        pass
        
    try:
        hints_server() # Execute function hints_server()
    except rospy.ROSInterruptException: # Keep going until keyboard exception (Ctrl+C)
        pass
