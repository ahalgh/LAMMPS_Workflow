def Thermal_calc(file,stepsize,NPTstep,delta,Thermal_type):
    #Can be used for both Compressability and thermal expansion since both depend on Volume as a function of either temperature or pressure
    import numpy as np
    import re

    #Number of steps in the .out file, depends on steps run and size
    stepcount = int(NPTstep / stepsize)
    
    #Adding One since lammps inserts a step at beginning and end
    stepcount += 2
    
    #Nine Thermal properties, specified by thermo custom command
    Thermo_prop = 9
    
    #Four Sims, 1 NVE equilibration, 3 NPT, 1 Normal, 1 @ + del, 1 @- del for finite difference
    sims = 4
    
    #initialize thermal_data matrix
    Thermal_data = np.zeros((stepcount,Thermo_prop,sims))

    #Reading in output of .out files and putting into thermal data
    x = 0
    counter = 0
    with open(file, 'r') as f:    
        for line in f:
            if 'Step Lx PotEng KinEng TotEng Temp Press Density Enthalpy' in line: 
                for line in f:
                    if "Loop time" in line:
                        x = 0
                        break
                    
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                    res = list(map(float, temp))
                    Thermal_data[x,:,counter] = res
                    x += 1 
                counter += 1
    
    #Cut off steps in the beginning to allow equilibrium, 1/10th of steps
    equilstep = int(stepcount*0.1)
    
    #Initial Mean Volume 
    V_init = sum(Thermal_data[equilstep:,1,1] ** 3) / len(Thermal_data[equilstep:,1,1])
    
    #Mean Volume at + delta 
    V_delplus = sum(Thermal_data[equilstep:,1,2] ** 3) / len(Thermal_data[equilstep:,1,1])

    #Mean Volume at - delta 
    V_delmin = sum(Thermal_data[equilstep:,1,3] ** 3) / len(Thermal_data[equilstep:,1,1])

    #Type to determine formula to use 
    if Thermal_type == 'Exp':
        a = 1/V_init * (V_delplus - V_delmin) / (2*delta)
        return a
    elif Thermal_type == 'Comp':
        B = -1/V_init * (V_delplus - V_delmin) / (2*delta)
        return B
    else:
        return 0

def Specific_H(file,stepsize,NPTstep,delta,sim_atoms):
    import numpy as np
    import re

    
    #Number of steps in the .out file, depends on steps run and size
    stepcount = int(NPTstep / stepsize)
    
    #Adding One since lammps inserts a step at beginning and end
    stepcount += 2
    
    #Nine Thermal properties, specified by thermo custom command
    Thermo_prop = 9
    
    #Four Sims, 1 NVE equilibration, 3 NPT, 1 Normal, 1 @ + del, 1 @- del for finite difference
    sims = 4
    
    #initialize thermal_data matrix
    Thermal_data = np.zeros((stepcount,Thermo_prop,sims))

    #Reading in output of .out files and putting into thermal data
    x = 0
    counter = 0
    with open(file, 'r') as f:    
        for line in f:
            if 'Step Lx PotEng KinEng TotEng Temp Press Density Enthalpy' in line: 
                for line in f:
                    if "Loop time" in line:
                        x = 0
                        break
                    
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                    res = list(map(float, temp))
                    #print(counter,res)
                    Thermal_data[x,:,counter] = res
                    x += 1 
                counter += 1
    
    equilstep = int(stepcount*0.1)
    
    #Mean Average Enthalpy in normal Conditions to check
    hnormal = sum(Thermal_data[equilstep:,8,1]) / len(Thermal_data[equilstep:,8,1])
    
    #Mean Average Enthalpy + del
    H_delplus = sum(Thermal_data[equilstep:,8,2]) / len(Thermal_data[equilstep:,8,2])
    
    #Mean Average Enthalpy - del
    H_delmin = sum(Thermal_data[equilstep:,8,3]) / len(Thermal_data[equilstep:,8,3])

    #Need to convert from Ev/sim*K to J/mol to check value
    Ev2J = 1.60218e-19
    mol = 6.02214076e23
    Evsim2Jmol = Ev2J / (sim_atoms/mol)
    
    H_delplus = H_delplus * Evsim2Jmol
    H_delmin = H_delmin * Evsim2Jmol
    
    SpecificH = (H_delplus - H_delmin) / (2*delta)
    
    return SpecificH
    
