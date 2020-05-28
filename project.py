import tkinter as tk
import matplotlib.pyplot as plt


def msToMPH(ms):
	#convert metres per second to mph
	conv = 2.237
	return ms*conv

def metresToFeet(m):
	#convert metres per second to mph
	conv = 3.281
	return m*conv

def Drag(vel,frontal_area):
	#Define the drag equation to calculate drag with an atmosphere
	#D = 0.5pV**2CA
	drag_coef = float(ent_drag_coef.get())
	air_density = 1.225
	D = 0.5*air_density*(vel**2)*drag_coef*frontal_area
	return D

def AccelerationWithDrag(thrust,vel,frontal_area,weight_at_start,prop_w_loss):
	#Calculate instantaneous acceleration with drag
	g=9.81
	if vel >= 0:
		acc = ((thrust - Drag(vel,frontal_area))/(weight_at_start-prop_w_loss))-g
	else:
		acc = -g
	return acc

def CreateMotorData(motor):
	#basic sample motor thrust time curves, taken from the National American Rocketry website
	#https://www.nar.org/standards-and-testing-committee/nar-certified-motors/
	#awkwardly the data is inside an unstructured pdf so hard coded here....
	#not the best solution but it works for the simulator
	#,0.534    0.000
	#Estest A8 Motor
	if motor == "A": data = "0.016    0.080,0.036    0.293,0.050    0.259,0.060    0.357,0.070    0.419,0.080    0.355,0.102    0.781,0.124    1.443,0.152    2.966,0.170    4.426,0.202    7.160,0.224    9.051,0.246    9.555,0.256    9.317,0.276    7.958,0.294    6.108,0.326    4.235,0.350    3.813,0.376    3.997,0.410    3.926,0.452    3.724,0.474    4.046,0.502    4.092,0.532    4.146"
	#Estes B6 Motor
	if motor == "B": data = "0.023    0.688,0.057    2.457,0.089    4.816,0.116    7.274,0.148    9.929,0.171    12.140,0.191    11.695,0.200    10.719,0.209    9.240,0.230    7.667,0.255    6.488,0.305    5.505,0.375    4.816,0.477    4.620,0.580    4.620,0.671    4.521,0.746    4.226,0.786    4.325,0.802    3.145,0.825    1.572"
	#Estes C6 Motor
	if motor == "C": data = "0.031    0.946,0.092    4.826,0.139    9.936,0.192    14.090,0.209    11.446,0.231    7.381,0.248    6.151,0.292    5.489,0.370    4.921,0.475    4.448,0.671    4.258,0.702    4.542,0.723    4.164,0.850    4.448,1.063    4.353,1.211    4.353,1.242    4.069,1.303    4.258,1.468    4.353,1.656    4.448,1.821    4.448,1.834    2.933,1.847    1.325"
	#Estes D11 Motor
	if motor == "D": data = "0.033    2.393,0.084    5.783,0.144    12.170,0.214    20.757,0.261    24.350,0.289    26.010,0.311    23.334,0.325    18.532,0.338    14.536,0.356    12.331,0.398    10.720,0.480    9.303,0.618    8.676,0.761    8.24,0.955    8.209,1.222    7.955,1.402    8.319,1.540    8.291,1.701    8.459,1.784    8.442,1.803    6.239,1.834    3.033"
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

def CreateBurnData(time,thrust,propellant_weight,liftoff_weight,frontal_area):
	velocity = []
	acceleration = []
	drag = []
	altitude = []

	v = 0
	t_old = 0
	s = 0
	prop_loss = propellant_weight/len(thrust)
	for i,t in enumerate(time):
		acc = AccelerationWithDrag(thrust[i],v,frontal_area,liftoff_weight,prop_loss)
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

def CreateCoastData(v,s,t,propellant_weight,liftoff_weight,frontal_area):
	#now carry on from these initial figures to a landing. Iinitialise iterator at 5 minutes
	coast_acceleration = []
	coast_altitude = []
	coast_velocity = []
	iterator = []
	second_count = t
	#calculate acceleration and alti for each .1s 
	#stop when the altitude is the ground
	while s >0:
		acc = AccelerationWithDrag(0,v,frontal_area,liftoff_weight,0)
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

def CalcAlt():
	liftoff_weight = float(ent_dry_weight.get())/1000
	propellant_weight = float(ent_prop_weight.get())/1000
	#convert diameter to frontal area using the circle equation pi r sqrd
	frontal_area = ((float(ent_diameter.get())/200)**2)*3.14159
	motor = motor_var.get()

	time,thrust = CreateMotorData(motor)
	velocity, acceleration,altitude, v,s,t = CreateBurnData(time,thrust,propellant_weight,liftoff_weight,frontal_area)

	coast_acceleration, coast_velocity, coast_altitude, iterator = CreateCoastData(v,s,t,propellant_weight,liftoff_weight,frontal_area)

	lbl_result['text'] = f"{max(coast_altitude):.2f}ft"

def BurnPlotClick():
	liftoff_weight = float(ent_dry_weight.get())/1000
	propellant_weight = float(ent_prop_weight.get())/1000
	#convert diameter to frontal area using the circle equation pi r sqrd
	frontal_area = ((float(ent_diameter.get())/200)**2)*3.14159
	motor = motor_var.get()


	time,thrust = CreateMotorData(motor)
	velocity, acceleration,altitude, v,s,t = CreateBurnData(time,thrust,propellant_weight,liftoff_weight,frontal_area)

	PlotBurnData(time,velocity,acceleration,altitude)

def FlightProfileClick():
	liftoff_weight = float(ent_dry_weight.get())/1000
	propellant_weight = float(ent_prop_weight.get())/1000
	#convert diameter to frontal area using the circle equation pi r sqrd
	frontal_area = ((float(ent_diameter.get())/200)**2)*3.14159
	motor = motor_var.get()


	time,thrust = CreateMotorData(motor)
	velocity, acceleration,altitude, v,s,t = CreateBurnData(time,thrust,propellant_weight,liftoff_weight,frontal_area)

	coast_acceleration, coast_velocity, coast_altitude, iterator = CreateCoastData(v,s,t,propellant_weight,liftoff_weight,frontal_area)

	PlotBurnToLandAlt(iterator,time,coast_altitude,altitude)

if __name__ == '__main__':

	m = tk.Tk()

	m.title("Model Rocket Calculator")

	frm_entry = tk.Frame(master = m)
	frm_btn = tk.Frame(master = m)
	
	# Create a Tkinter variable
	motor_var = tk.StringVar(m)

	# Dictionary with options
	motor_choices = { 'A','B','C','D'}
	motor_var.set('A') # set the default option

	popupMenu = tk.OptionMenu(frm_entry, motor_var, *motor_choices)
	tk.Label(frm_entry, text="Choose a Estes Sample Motor").grid(row = 5, column = 0)
	popupMenu.grid(row = 5, column =1)

	# on change dropdown value
	def change_dropdown(*args):
	    print( motor_var.get() )

	# link function to change dropdown
	motor_var.trace('w', change_dropdown)

	#Dry weight
	lbl_weight_name = tk.Label(master = frm_entry,text = "Dry model weight")
	ent_dry_weight = tk.Entry(master = frm_entry, width = 10)
	lbl_dry_weight = tk.Label(master = frm_entry, text = "g")
	lbl_weight_name.grid(row = 0, column = 0)
	ent_dry_weight.grid(row = 0, column  = 1, sticky = 'e')
	lbl_dry_weight.grid(row = 0, column = 2, sticky = 'w')

	#Frontal Area
	lbl_diam_name = tk.Label(master = frm_entry,text = "Rocket Diameter")
	ent_diameter = tk.Entry(master = frm_entry, width = 10)
	lbl_diam = tk.Label(master = frm_entry, text = "cm")
	lbl_diam_name.grid(row = 1, column = 0)
	ent_diameter.grid(row = 1, column  = 1, sticky = 'e')
	lbl_diam.grid(row = 1, column = 2,sticky = 'w')

	#propellant weight
	lbl_prop_name = tk.Label(master = frm_entry,text = "Propellant Weight")
	ent_prop_weight = tk.Entry(master = frm_entry, width = 10)
	lbl_prop_weight = tk.Label(master = frm_entry, text = "g")
	lbl_prop_name.grid(row = 2, column = 0)
	ent_prop_weight.grid(row = 2, column  = 1, sticky = 'e')
	lbl_prop_weight.grid(row = 2,column = 2,sticky = 'w')

	#Drag coefficient
	lbl_drag_coef_name = tk.Label(master = frm_entry,text = "Drag coefficient")
	ent_drag_coef = tk.Entry(master = frm_entry, width = 10)
	lbl_drag_coef = tk.Label(master = frm_entry, text = "")
	lbl_drag_coef_name.grid(row = 3, column = 0)
	ent_drag_coef.grid(row = 3, column  = 1, sticky = 'e')
	lbl_drag_coef.grid(row = 3,column = 2,sticky = 'w')
	

	btn_altitude = tk.Button(master = frm_btn, text = "Estimate Altitude", command = CalcAlt)
	lbl_result = tk.Label(master = frm_btn, text = "Altitude")
	btn_altitude.grid(row = 0, column = 0)
	lbl_result.grid(row= 0, column = 1)
	
	btn_burn_plot = tk.Button(master = frm_btn, text = "Create the burn plot", command = BurnPlotClick)
	btn_burn_plot.grid(row = 1, column = 0)

	btn_profile_plot = tk.Button(master = frm_btn, text = "Create the profile plot", command = FlightProfileClick)
	btn_profile_plot.grid(row = 2, column = 0)

	frm_entry.grid(row=0, column=0, padx=10)

	frm_btn.grid(row=0, column=1)

	#lbl_result.grid(row=0, column=2, padx=10)

	m.mainloop()