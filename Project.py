import matplotlib.pyplot as plt

def VelocityMax(liftoff_weight, total_impulse):
	#take the impulse in Newtown Seconds and divide it
	#by the mass to give the max vleocity at the end
	#of the burn V = I/m
	vel_max = total_impulse/liftoff_weight
	return vel_max

def msToMPH(ms):
	#convert metres per second to mph
	conv = 2.237
	return ms*conv

def metresToFeet(m):
	#convert metres per second to mph
	conv = 3.281
	return m*conv

def BurnoutAltitude(vel_max,dur_of_thr):
	#take the max thrust, work out the average velocity (Vav = (V1+V2)/2)
	#use newtownian equation for distance S = Vt
	#this is in metres but aviation is done in feet so convert
	avg_vel = vel_max/2
	dist = avg_vel*dur_of_thr
	return metresToFeet(dist)

def CoastingAltitude(vel_max):
	#use newtownian physics again 2as = v2^2 - v1^2
	#v2 == max vel (at burnout)
	#v1 == 0 at appogee so 2as == v2^2  // s == v2^2/(2a)
	#a == acceleration which is just gravity
	g = 9.81
	coast_alt = vel_max**2/(2*g)
	return metresToFeet(coast_alt)

def Drag(vel,drag_coef,frontal_area,air_density):
	#Define the drag equation to calculate drag with an atmosphere
	#D = 0.5pV**2CA
	D = 0.5*air_density*(vel**2)*drag_coef*frontal_area
	return D

def AccelerationWithDrag(thrust,air_density,vel,drag_coef,frontal_area,weight_at_start,prop_w_loss):
	#Calculate instantaneous acceleration with drag
	g=9.81
	if vel >= 0:
		acc = ((thrust - Drag(vel,drag_coef,frontal_area,air_density))/(weight_at_start-prop_w_loss))-g
	else:
		acc = -g
	return acc

def PrintNewtonianPhysics(total_impulse,liftoff_weight,duration_of_thrust):
	#Print the basics of the purely newtonian model
	#No aerodynamic drag and constant thrust
	vel_max = VelocityMax(liftoff_weight,total_impulse)
	vel_max_mph = msToMPH(vel_max)
	print("Simple equations for model rocket example using newtonian physics\nAssuming no aerodynamic affects and constant thrust")
	print (f"Max velocity (at burnout) = {vel_max:.1f} ms^-1 == {vel_max_mph:.1f} mph")

	burnout_alt = BurnoutAltitude(vel_max,duration_of_thrust)
	print (f"Height at burnout = {burnout_alt:.0f} ft")

	coast_alt = CoastingAltitude(vel_max)
	print (f"Coasting Altidue = {coast_alt:.0f} ft")

	max_alt = burnout_alt + coast_alt
	print (f"Maxiumum Altitude = {max_alt:.0f} ft")

def CreateMotorData(motor):
	#basic sample motor thrust time curves, taken from the National American Rocketry website
	#https://www.nar.org/standards-and-testing-committee/nar-certified-motors/
	#awkwardly the data is inside an unstructured pdf so hard coded here....
	#not the best solution but it works for the simulator
	
	#Estest A8 Motor
	if motor == "A": data = "0.016    0.080,0.036    0.293,0.050    0.259,0.060    0.357,0.070    0.419,0.080    0.355,0.102    0.781,0.124    1.443,0.152    2.966,0.170    4.426,0.202    7.160,0.224    9.051,0.246    9.555,0.256    9.317,0.276    7.958,0.294    6.108,0.326    4.235,0.350    3.813,0.376    3.997,0.410    3.926,0.452    3.724,0.474    4.046,0.502    4.092,0.532    4.146,0.534    0.000"
	#Estes B6 Motor
	if motor == "B": data = "0.023    0.688,0.057    2.457,0.089    4.816,0.116    7.274,0.148    9.929,0.171    12.140,0.191    11.695,0.200    10.719,0.209    9.240,0.230    7.667,0.255    6.488,0.305    5.505,0.375    4.816,0.477    4.620,0.580    4.620,0.671    4.521,0.746    4.226,0.786    4.325,0.802    3.145,0.825    1.572,0.860    0.000"
	#Estes C6 Motor
	if motor == "C": data = "0.031    0.946,0.092    4.826,0.139    9.936,0.192    14.090,0.209    11.446,0.231    7.381,0.248    6.151,0.292    5.489,0.370    4.921,0.475    4.448,0.671    4.258,0.702    4.542,0.723    4.164,0.850    4.448,1.063    4.353,1.211    4.353,1.242    4.069,1.303    4.258,1.468    4.353,1.656    4.448,1.821    4.448,1.834    2.933,1.847    1.325,1.860    0.000"
	#Estes D11 Motor
	if motor == "D": data = "0.033    2.393,0.084    5.783,0.144    12.170,0.214    20.757,0.261    24.350,0.289    26.010,0.311    23.334,0.325    18.532,0.338    14.536,0.356    12.331,0.398    10.720,0.480    9.303,0.618    8.676,0.761    8.24,0.955    8.209,1.222    7.955,1.402    8.319,1.540    8.291,1.701    8.459,1.784    8.442,1.803    6.239,1.834    3.033,1.860    0.000"
	#do an split on the data using list comprehension
	thrust_data = [i.split("    ") for i in data.split(",")]

	#sort out the time and thrust elements
	time = [float(thrust_data[i][0]) for i in range(0,len(thrust_data))]
	thrust = [float(thrust_data[i][1]) for i in range(0,len(thrust_data))]
	#drag = [AccelerationWithDrag(thrust,1.225,)]
	#plot the thrust curve

	return time, thrust

def PlotMotorData(time,thrust):
	plt.plot(time, thrust)
	plt.title("Burn characteristics of motor")
	plt.ylabel("Thrust (nm^-1s")
	plt.xlabel("Time since start of burn (s)")
	plt.show()

def CreateBurnData(time,thrust):
	velocity = []
	acceleration = []
	drag = []
	altitude = []

	v = 0
	t_old = 0
	s = 0
	prop_loss = propellant_weight/len(thrust)
	for i,t in enumerate(time):
		acc = AccelerationWithDrag(thrust[i],1.225,v,0.7,frontal_area,liftoff_weight,prop_loss)
		if acc < 0: acc = 0
		acceleration.append(acc)
		t_diff = t-t_old
		v = v + (acc*t_diff)
		velocity.append(v)
		s = s+ v*t_diff
		altitude.append(metresToFeet(s))
		t_old = t
	return velocity, acceleration, altitude, v, s, t

def PlotBurnData(time,velocity,acceleration,altitude):
	plt.plot(time,velocity, label = 'Velocity ($ms^{-1}$)')
	plt.plot(time,acceleration, label = 'Acceleration ($ms^{-2}$)')
	plt.plot(time,altitude, label = 'Altitude (ft)')
	plt.title("Initial Burn flight characteristics")
	plt.ylabel("Value")
	plt.xlabel("Time (s)")
	plt.legend()
	plt.show()

def CreateCoastData(v,s,t):
	#now carry on from these initial figures to a landing. Iinitialise iterator at 5 minutes
	coast_acceleration = []
	coast_altitude = []
	coast_velocity = []
	iterator = []
	second_count = t
	#calculate acceleration and alti for each .1s 
	#stop when the altitude is the ground
	prop_loss = propellant_weight/len(thrust)
	while s >0:
		acc = AccelerationWithDrag(0,1.225,v,0.7,0.0007,liftoff_weight,prop_loss)
		coast_acceleration.append(acc)
		v = v + (acc*0.1)
		coast_velocity.append(v)
		s = s+ v*0.1
		coast_altitude.append(metresToFeet(s))
		second_count += 0.1
		iterator.append(second_count)
	return coast_acceleration, coast_velocity, coast_altitude, iterator

def PlotBurnToLandAlt(iterator,time,coast_altitude,altitude):
	
	plt.plot(time+iterator,altitude+coast_altitude, label = 'Altitude (ft)')
	plt.title("Profile of flight")
	plt.xlabel("Time (s)")
	plt.ylabel("Altitude (ft)")
	plt.show()

if __name__ == '__main__':
	#Set these for Netownian Physics if required
	total_impulse = 4.85
	duration_of_thrust = 1.03

	#in Kgs
	liftoff_weight = 0.10
	#in area use pi.r**2 
	frontal_area = 0.0007
	#in kg
	propellant_weight = 0.006
	#Motor can be A,B,C or D
	motor = 'D'
	burnout_weight = liftoff_weight - propellant_weight

	#Set the thrust curve from the chosen motor above
	time,thrust = CreateMotorData(motor)

	#Using the thrust curve to produce a list of the Velocity, Acceleration and Altitude per second
	#v, s and t are the final velocity, altitude and time at the end of the burn 
	velocity, acceleration, altitude, v, s, t = CreateBurnData(time,thrust)
 
 	#make a graph showing the details during the burn
	PlotBurnData(time, velocity, acceleration, altitude)

	#Produce lists of the velocity, altitude and time from the end of the burn
	#to the landing of the rocket
	coast_acceleration, coast_velocity, coast_altitude, iterator = CreateCoastData(v,s,t)

	#plot the altitude curve
	PlotBurnToLandAlt(iterator, time, coast_altitude, altitude)
