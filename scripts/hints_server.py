#!/usr/bin/env python

import rospy
import random # This library is needed to computed random numbers
from numpy import random

from assignment1_solution.srv import hints, hintsResponse # Import custom service of type goal

global hints_list

		
hints_list = ['','','','','','','','','','','','','','','','','','',''] # Create empty list

def create_random_hints(): # This function associate hints with IDs

	informations =[ ('who, Rev.Green'		), # List with all the possible hints
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

	n = 1 # Define counter
	index = 1 # Define index
	while (n < 18):
		ID = list("ID0, ")
		ID[2] = str(index)
		CurrentID = "".join(ID) # Creates a string made of ID'index' where index is the number of the current ID
		for i in range (0, 3):
			selection = random.choice(informations)
			hints_list[n+i] = CurrentID + (selection) # Associate one random hint with the current ID
			informations.remove(selection) # Remove the selected hint from the informations list
			print(hints_list[n+i])
		n = n + 3 # Change ID number after 3 hints are associated
		index = index + 1 # Update index

	n = 1 # Reset counter
	index = 1 # Reset index
	consistent = 0 # Define consistent
	
	while (n<18): # Inside this loop we check if there is at least one consistent hypothesis
		
		index = 1
			
		if ((("who" in hints_list[n])or("who" in hints_list[n+1])or("who" in hints_list[n+2]))and
		    (("what" in hints_list[n])or("what" in hints_list[n+1])or("what" in hints_list[n+2]))and
		    (("where" in hints_list[n])or("where" in hints_list[n+1])or("where" in hints_list[n+2]))):
	
			print("A consistent hint was generated")
			print(hints_list[n:n+3])
			consistent += 1
			rospy.set_param('/correct_HP0', (int((n+2)/3))) # When a consistent hypothesis if found it can be set as the correct one, in the parameter server
			break # end the cycle
		else:
			print("This hypothesis is unconsistent")
			print(hints_list[n:n+3])
			if((n==16)and(consistent == 0)): # No consistent hypothesis is found,
				create_random_hints()	# so start the function from the top
			
		n = n + 3	
		index = index + 1
	

def handle_hints_generator(req): # Callback of the service
	if(req.request is True): # The request sent by the client is a bool
				 # If it is True than the robot entered a room and must receive an hint
		
		if( len(hints_list) > 0):
			hint = random.choice(hints_list) # Pick a random hint from the list
			hints_list.remove(hint) # Remove the hint just picked from the list, in order to avoid picking it again
		else:
			hint = 'No more hints! all have been found' # In case there are no hints left
		
		return hintsResponse(hint) # Returns the hint generated

def hints_server():
	rospy.init_node('hints_server') # Initialize the node as hints_server
	s = rospy.Service('hints_generator', hints, handle_hints_generator) # The nodes works as a server for the
								 	     # service hints_generator

	print("\n")
	print("Waiting for requests:") # Once the node is started, print to screen so that
					# the user knows it is waiting for requests

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
