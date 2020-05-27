# Model-Rocket-Sim
A python based mathematical physics simulator for model rocketry.

It takes the variables of a model rocket and outputs either 
  a) the basic physics from Netown's laws without aerodynamics - max velocity, max alt
  b) two sets of plots, one of the burn characteristics and one of the full flight profile

In the bottom of the code in the main function are the global rocket variables that can be set:

  These are for the basic newtonian physics:
  
  
	total_impulse = Newton metres per second of the motor
	duration_of_thrust = in seconds
  
  These are for the shared variables:
  
  
	liftoff_weight = in kgs
	frontal_area = in metres squared
	propellant_weight = in kgs
  
  There are 4 motor profiles taken from the NAR website and hard-coded
	these are used for aerodynamic profile:
	
	
  motor = Motor can be A,B,C or D
