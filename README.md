# mtg_mechanism
Electromechanical system code

All of this code must be on the rpi:
circuit_helper - central code for the circuit, links all the components. Actuonix is triggered by first two limit switches, third limit switch triggered by actuonix, sends commands to the other robot. 
circuit_fsm - controls the circuit based on what the centralized system says 

This code is on centralized compute and rpi:
client.py - code to SEND flags (to specific IP)
server.py - code to RECEIVE flags (to general address)

This is just on centralized compute:
central_compute_node.py - ROS wrapper for comms stuff

Other code: 
test_(component_name) - Used to check that one component is working
