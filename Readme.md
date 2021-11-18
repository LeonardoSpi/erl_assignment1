## Overview

This package was developed as a solution of the first assignment of the Experimental Robotics Laboratory course of Robotics Engineering held by Professors Buoncompagni Luca and Recchiuto Carmine. The package recreates the ontology of cluedo boardgame, while a robot reach random goals in a 2d space in ros stage.


### Licence

**Author: Leonardo Spinelli<br/>
Affiliation: University of Genoa<br />
Maintainer: Leonardo Spinelli, leonardo.spinelli91@gmail.com**

The erl_assignment1 package has been tested under ROS Melodic on Ubuntu 16.04.6 LTS.

## Architecture

![](architecture.jpg)

The main node is **robot_controller** which works as a FSM. The controller asks to the **goal_server** for random positions to acquire in the ros stage environment. The request is a bool while the response from the server comes as a couple of float describing x and y positions. The idea is to simulate the player of cluedo reaching different rooms to find hints, in this case the rooms are exploited as random positions. Once a goal is reached, the robot_controller retrives an hint from the **hints_server**. 

### Building from source

To build from source, clone the latest version from this repository into your catkin workspace and compile the package using:

	cd catkin_workspace/src
	git clone https://github.com/LeonardoSpi/erl_assignment1
	cd ..
	catkin_make

Remember to make scripts executable, in the scripts folder use the following commands:

	chmod +x robot_controller.py
	chmod +x goal_server.py
	chmod +x hints_server.py
	
Check files permission with:
	
	ls -l

## Usage

To run the solution you can use the solution.launch file:

	roslaunch erl_assignment1 erl_assignment1.launch

## Launch files

* **erl_assignment1.launch** This launch file will starts 4 nodes: stage, hints_server, goal_server, robot_controller.

	- **'stage'** Spawn the robot in the ros stage environment.

	- **'hints_server'** Start a service server node which will generate a random goal between (-6,6) when requested.

	- **'goal_server'** Start service client that asks the server for a goal and then commands the robot to reach it. Respawn and output are set to True, so that the once a goal is reached the client will send another request and the output will be printed to screen.

	- **'robot_controller'** Start service client that asks the server for a goal and then commands the robot to reach it. Respawn and output are set to True, so that the once a goal is reached the client will send another request and the output will be printed to screen.

## Custom Nodes

### Server

Waits for requests in order to generate random x and y coordinates in the interval (-6, 6)

#### Subscribed Topics

None

#### Published Topics

None

#### Services

* **`goal_generator`** ([assignment1_solution/goal])

	Returns a random goal in x and y coordinates in the interval (-6, 6). The service takes as a request a 		bool, if it is True it generates the random goal responding with two floats: x and y. If the request is 	False than the goal is set to x=0, y=0, the robot comes back to the starting position.

### Client

Asks to the server for a random goal. Moves the robot using a specific law of motion which is described in the graphs below.

![](it.plot.png)

- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Displacement function
- ![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+) Velocity function
- ![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+) Acceleration function

The function has been developed with the intent to have 0 initial and final velocities and accelerations for both axis.

#### Subscribed Topics

* **`/odom`** ([nav_msgs.msg/Odometry])

	The current position of the robot.

#### Published Topics

* **`/cmd_vel`** ([geometry_msgs.msg/Twist])

	The current robot velocities.

#### Services

* **`goal_generator`** ([assignment1_solution/goal])

	Request goal
 


