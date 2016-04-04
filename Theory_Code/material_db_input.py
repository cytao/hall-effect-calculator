###	material_db_input.py
###	Input new material electrical properties for "Hall Effect" experiment
###	Nagel lab
###	by Chiao-Yu Tao
###	Last edited: 2016/03/31

import yaml, sys
from const_n_func import Material
from blitzdb import Document,FileBackend

def main():
	backend = FileBackend("./my-db") #locate the backend

	fin = file("Cu_material_db.yaml","r") #read the yaml file
	in_param = yaml.load(fin) #load it
	name = in_param.get("Name") #extract out the parameters
	cond = in_param.get("Conductivity") 
	n = in_param.get("Carrier_Density") 
	supercond = in_param.get("Superconductivity")
	res = in_param.get("Resistance")

	right_input_flag = True #check the superconducting type matches the number of critical fields
	if supercond.get("Superconducting"): #create a new entry for a superconductor
		right_input_flag = False if len(supercond.get("Critical_Fields")) != supercond.get("Type")  else True
		if right_input_flag:
			new = Material({"name": name, "cond": cond, "n": n,  
					"sc": supercond.get("Superconducting"),
					"sctype" : supercond.get("Type"),
					"Tc" : supercond.get("Critical_Temperature"),
					"nc" : supercond.get("Critical_Current_Density"),
					"Hc" : supercond.get("Critical_Fields"),
					"L" : supercond.get("Penetration_Depth"),
					"Tref" : res.get("Ref_Temperature"),
					"res" : res.get("Resistivity"),
					"alpha" : res.get("Temperature_Coefficient")
					})
		else:
			print "Superconducting type and number of critical fields don't match!"
	else: #create a new entry for a non-superconductor
		new = Material({"name": name, "cond": cond, "n": n,  
				"sc": supercond.get("Superconducting"),
				"Tref" : res.get("Ref_Temperature"),
				"res" : res.get("Resistivity"),
				"alpha" : res.get("Temperature_Coefficient")
				})
		
	if right_input_flag:
		new.save(backend) #save the entry in the database
		#always update the database when there's an old entry of this material in the database
		mtrl = backend.filter(Material, {"name":name})
		mtrl.delete()
		backend.commit()
		print "Input succeeded!"

if __name__ == '__main__':
	main()
