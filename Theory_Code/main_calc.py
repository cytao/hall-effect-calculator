###     main_calc.py
###     Calculation of signal and magnetica Hall potential for "Hall Effect" experiment
###     Nagel lab
###     by Chiao-Yu Tao
###     Last edited: 2016/04/01

import yaml, sys, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from blitzdb import Document,FileBackend
from const_n_func import *

def main():
	backend = FileBackend("./my-db") #locate the database
	fin = file("Cu_calc_input.yaml","r") #read the yaml file
	in_param = yaml.load(fin) #load it
	material = in_param.get("Material") #extract the parameters
	circuit_param = in_param.get("Circuit_Design")
	exp_param = in_param.get("Experimental_Setup")
	step = in_param.get("Output").get("Current_Sweep_Step")

	c_w = circuit_param.get("Width")
	c_R = circuit_param.get("Radius")
	c_t = circuit_param.get("Thickness")
	c_w_else = circuit_param.get("Width_Else")
	c_l_else = circuit_param.get("Length_Else")

	file_str = "%s_w_%d_um_R_%d_um_t_%d_nm" %(material, c_w*1e6, c_R*1e6, c_t*1e9) #set the output file
	fout = file(file_str+".txt","w")
	
	mtrl = backend.get(Material, {"name": material}) #find the material information in the database
	print mtrl.name
	x = c_w/c_R #w/R ratio

	##########LIQUID NITROGEN TEMPERATURE CASE################

	#calculate the resistance of the trace to determine current upper limit
	trace_res_77 = CALC_RES(c_w, c_R, c_t, c_w_else, c_l_else, 77., mtrl.Tref, mtrl.res, mtrl.alpha) 
	current_limit_77 = min(exp_param.get("Current_Limit"), exp_param.get("Voltage_Limit")/trace_res_77) 
	
	#calculate the signals
	output_77 =  np.tile(np.arange(0,current_limit_77,step),(3,1)).transpose() #currents, V_G, V_S
	for i in range(0,output_77.shape[0]):
		output_77[i,1] = SIG_NORMAL(mtrl.n, c_w, c_t, output_77[i,0])*MODEL_CRC(x)
		output_77[i,2] = HALL_POT(mtrl.n, c_w, c_t, output_77[i,0])*MODEL_LIN(x)
	#Plot the data
	plt.ioff()
	fig = plt.figure()
	plt.plot(output_77[:,0],output_77[:,1], label=r"$V_G$ (77K)", marker="x",linestyle="None",color="k")
	plt.plot(output_77[:,0],output_77[:,2], label=r"$V_H$ (77K)", marker="+",linestyle="None",color="k")

	#Store the data
	fout.write("##########LIQUID NITROGEN TEMPERATURE CASE################\n")
	res_str = "Resistance = %.2e ohm\n\n" %trace_res_77
	fout.write(res_str)
	fout.write("I(A)\tV_G(V)\tV_H(V)\n")
	np.savetxt(fout,output_77,fmt="%.2e")


	##########ROOM TEMPERATURE CASE################

	trace_res_293 = CALC_RES(c_w, c_R, c_t, c_w_else, c_l_else, 293., mtrl.Tref, mtrl.res, mtrl.alpha) 
	current_limit_293 = min(exp_param.get("Current_Limit"), exp_param.get("Voltage_Limit")/trace_res_293) 

	output_293 =  np.tile(np.arange(0,current_limit_293,step),(3,1)).transpose() #currents, V_G, V_S
	for i in range(0,output_293.shape[0]):
		output_293[i,1] = SIG_NORMAL(mtrl.n, c_w, c_t, output_293[i,0])*MODEL_CRC(x)
		output_293[i,2] = HALL_POT(mtrl.n, c_w, c_t, output_293[i,0])*MODEL_LIN(x)

	plt.plot(output_293[:,0],output_293[:,1], label=r"$V_G$ (Room Temp.)", marker="s",mfc="None",linestyle="None",color="k")
	plt.plot(output_293[:,0],output_293[:,2], label=r"$V_H$ (Room temp.)", marker="D",mfc="None",linestyle="None",color="k")

	fout.write("\n##########ROOM TEMPERATURE CASE################\n")
	res_str = "Resistance = %.2e ohm\n\n" %trace_res_293
	fout.write(res_str)
	fout.write("I(A)\tV_G(V)\tV_H(V)\n")
	np.savetxt(fout,output_293,fmt="%.2e")

	
	##########SUPERCONDUCTING CASE################
	if mtrl.sc:
		output_sc =  np.tile(np.arange(0,exp_param.get("Current_Limit"),step),(2,1)).transpose() #currents, V_G, V_S
		for i in range(0,output_sc.shape[0]):
			output_sc[i,1] = SIG_SC(mtrl.L, c_w, c_t, output_sc[i,0])*MODEL_SCCJ(x)

		plt.plot(output_sc[:,0],output_sc[:,1], label=r"$V_G$ (Supercond.)",color="k")

		fout.write("\n##########SUPERCONDUCTING CASE################\n")
		fout.write("I(A)\tV_G(V)\n")
		np.savetxt(fout,output_sc,fmt="%.2e")

	#plot details
	plt.xlabel("Input current (A)",fontsize="15")
	plt.ylabel("Potential difference (V)",fontsize="15")
	plt.yscale("log")
	plt.title(material)
	plt.legend(loc=4)
	plt.savefig(file_str+".png",dpi=300,format="png")
	plt.close(fig)

	fin.close()
	fout.close()

if __name__ == '__main__':
	main()
