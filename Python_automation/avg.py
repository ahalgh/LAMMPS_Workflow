# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 14:02:29 2021

@author: ahalg
"""

#Calculate average from last 1000 steps of simulation in order to calculate more accurate values

def avg(file,stepsize,NPTstep,delta,Therm_prop, Thermo_num):
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
    Thermal_data = np.zeros((stepcount,Thermo_num,sims))

    
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
    
    if 'Lx' == Therm_prop: 
        index = 1
    elif 'PotEng' == Therm_prop:
        index = 2
    elif 'KinEng' == Therm_prop:
        index = 3
    elif 'TotEng' == Therm_prop:
        index = 4
    elif 'Temp' == Therm_prop:
        index = 5
    elif 'Press' == Therm_prop:
        index = 6
    elif 'Density' == Therm_prop:
        index = 7
    elif 'Enthalpy' == Therm_prop:
        index = 8
    else:
        index = 0;
        print("incorrect thermotype provided")           
    
                
                
                
    end_avg = sum(Thermal_data[-10:,index,1]) / 1000



