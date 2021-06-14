def main():
    import numpy as np
    import time
    from Pygraphs import Ev_graph,Bulk_graph,Finite_graph
    import os
    import sys
    path = os.getcwd()
    Full_tic = time.perf_counter()
    min_tic = time.perf_counter()
    #Python Script for automation of properties
    
    #Need to figure out how to pass in potential file to actual lammps code
    
    potential,pair_style,Type,stable_structure,lattice_guess,temp_low,temp_high,temp_del,deltatemp,deltapres,NPTstep,lat_size,fout_name = Read_input_file('./Input_potential/User_input.txt')
    print(fout_name)
    fout_name = os.path.join(path, "Outputs/",str(fout_name))
    #ofile = open(fout_name, "w")
    #ofile.write('Properties of ' , potential , 'Potential File:\n\n')
    
    Var_txt(pair_style,'pairsty.txt')
    Var_txt(lattice_guess,'lattice_guess.txt')
    Var_txt(potential,'potential.txt')
    Var_txt(Type,'type.txt')
    Var_txt(stable_structure,'stable.txt')
    
    
    #lammps_ver = "lammps/30Apr19"
    #Optimize, 0K
    lat_const = Optimizelattice()
    min_toc = time.perf_counter()
    #ofile.write("Lattice Constant: ",lat_const,f"Took {toc - tic:0.4f} seconds")
    finite_tic = time.perf_counter()
    #Optimize, finite temps
    
    temps = np.arange(temp_low,temp_high,temp_del)
    room_temp = 301.0;
    
    
    lat_temp = Optimizelattice_finite(temps)
    if room_temp in temps:
        result = np.where(room_temp == temps)
        room_temp_loc = int(result[0])
        lat_room = lat_temp[room_temp_loc,1]
        not_in_temps = False
    else:
        lat_room = Optimizelattice_finite([room_temp])
        lat_room = lat_room[0,1]
        Var_txt(lat_room,"lat_const.txt")
        Bulk_room = Bulk_prop(room_temp)
        not_in_temps = True
        print(Bulk_room)
    
    Finite_graph(lat_temp,potential)
    
    #Format a big table of all bulk constants over temperature 
    Var_txt(lat_const,"lat_const.txt")
    Bulk_0K = Bulk_prop(0)
    Bulk_finite = np.zeros((8,len(lat_temp)),dtype=float)
    
    
    for i in range(0,len(lat_temp)):
        #Passes the bulk_finite function the correct lattice parameter for the temperature
        Var_txt(lat_temp[i,1],"lat_const.txt")
        Bulk_finite[0,i] = lat_temp[i,0]
        Bulk_finite[1:,i] = Bulk_prop(lat_temp[i,0])
        

    Bulk_graph(Bulk_prop,potential)
    bulk_toc = time.perf_counter()
    
    #Initizing all these variables from indexes for readability
    Temp = Bulk_finite[0,:]
    lattice = lat_temp[:,1]
    C11 = Bulk_finite[1,:]
    C12 = Bulk_finite[2,:]
    C44 = Bulk_finite[3,:]
    Bulk_mod = Bulk_finite[4,:]
    Shear_mod1 = Bulk_finite[5,:]
    Shear_mod2 = Bulk_finite[6,:]
    Poisson_R = Bulk_finite[7,:]
    
    
    
        
    
    Ev_mat = EV_curves()
    #print(Ev_mat)
    
    Ev_graph(Ev_mat,potential)
    #toc = time.perf_counter()
    def_tic = time.perf_counter()
    Var_txt(lat_const,"lat_const.txt")
    Vac_Energy,Int_Energy = Pt_defect_prop()
    
    
    def_toc = time.perf_counter()
    cond_tic = time.perf_counter()
    
    #Always evaluate at 300 K
    Var_txt(lat_room ,"lat_const.txt")
    
    cond = Thermal_cond(room_temp)
    cond_toc = time.perf_counter()
    
    Exp_tic = time.perf_counter()
    
    
    
    temp = 300
    Therm_exp,SpecificH = ThermExp_SpecificH(NPTstep, deltatemp, lat_size, stable_structure,temp)

    pres = 1
    B = Iso_comp(NPTstep, deltapres, lat_size,pres)
    comp_toc = time.perf_counter()

    
    with open(fout_name, 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print('Properties of ' , potential.strip('\n') , 'Potential File:\n\n')
        print("Lattice minimization @ 0 [K]:")
        decorate(30)
        print("Lattice Constant: ",lat_const,f"\nTook {min_toc - min_tic:0.4f} seconds, Total: {min_toc - Full_tic:0.4f}\n")
        
        print("Lattice Constant and Elastic Properties Over Temperature:\n")
        
        #Formatting a table of all values
        tab_length = 210
        no_flag = True
        decorate(tab_length)
        print(' | {0:^20s} | {1:^20s} | {2:^20s} | {3:^20s} | {4:^20s} | {5:^20s} | {6:^20s} | {7:^20s} | {8:^20s} | '.format('Temperature [K]', 'Lat Parameter [Å]', 'C11 Constant [GPa]','C12 Constant [GPa]','C44 Constant [GPa]','Bulk Modulus [GPa]', 'Shear Mod 1 [GPa]','Shear Mod 2 [GPa]','Poisson Ratio'))
        decorate(tab_length)
        print(' | {0:^20f} | {1:^20f} | {2:^20f} | {3:^20f} | {4:^20f} | {5:^20f} | {6:^20f} | {7:^20f} | {8:^20f} | '.format(0,lat_const,Bulk_0K[0],Bulk_0K[1] ,Bulk_0K[2] ,Bulk_0K[3] ,Bulk_0K[4] ,Bulk_0K[5] ,Bulk_0K[6]))
        for i in range(0,len(lat_temp)):
            if Temp[i] >= 300 and no_flag and not_in_temps:
                no_flag = False
                print(' | {0:^20f} | {1:^20f} | {2:^20f} | {3:^20f} | {4:^20f} | {5:^20f} | {6:^20f} | {7:^20f} | {8:^20f} | '.format(300,lat_room,Bulk_room[0],Bulk_room[1] ,Bulk_room[2] ,Bulk_room[3] ,Bulk_room[4] ,Bulk_room[5] ,Bulk_room[6]))
            print(' | {0:^20f} | {1:^20f} | {2:^20f} | {3:^20f} | {4:^20f} | {5:^20f} | {6:^20f} | {7:^20f} | {8:^20f} | '.format(Temp[i],lattice[i],C11[i] ,C12[i] ,C44[i] ,Bulk_mod[i] ,Shear_mod1[i] ,Shear_mod2 [i], Poisson_R[i]))
        decorate(tab_length)
        print(f'\nTook {bulk_toc - finite_tic:0.4f} seconds, Total: {bulk_toc - Full_tic:0.4f}\n')
        
        print("Energies of Defect Formation:")
        decorate(30)
        print("Vacancy: ",Vac_Energy,"\nInterstitial: ",Int_Energy,f"\nTook {def_toc - def_tic:0.4f} seconds, Total: {def_toc - Full_tic:0.4f}\n")
        
        print("Transport Properties:")
        decorate(30)
        print("Thermal Conductivity: ",cond,f"\nTook {cond_toc - cond_tic:0.4f} seconds, Total: {cond_toc - Full_tic:0.4f} seconds\n")
        
        print("Thermal Properties:")
        decorate(30)
        print("Thermal Expansivity: ",Therm_exp," [1/K]\nIsothermal Compressibility: ",B,"[1/bar]\nSpecific Heat Capacity: ",SpecificH,f" [J/mol*K]\nTook {comp_toc - Exp_tic:0.4f} seconds, Total: {comp_toc - Full_tic:0.4f}\n")
        sys.stdout = sys.stdout
    
    global txt_list
    txt_list.add('BulkProp_0K.txt')
    txt_list.add('BulkProp_finite.txt')
    for i in txt_list:
        os.remove(i)
        
    #os.remove('lattice_guess.txt')
    #os.remove('potential.txt')
    #os.remove('type.txt')
    #os.remove('stable.txt')
    #os.remove('pairsty.txt')
    #os.remove('lat_size.txt')
    #os.remove('pres.txt')
    #os.remove('deltapres.txt')
    #os.remove("lat_temp.txt")
    #os.remove("temp.txt")
    #os.remove("timesteplength.txt")
    #os.remove("deltatemp.txt")
    #os.remove("lat_const.txt")
    #os.remove("BulkProp_0K.txt")
    #os.remove("BulkProp_finite.txt")
    #os.remove("constant.txt")
    
    
    
    
    


def runLammps(lammps_input_name,in_location,lammps_output_name,log_name):
    import subprocess as sp
    import os
    path = os.getcwd()
    in_file = os.path.join(path, 'LAMMPS_scripts/'+ in_location,lammps_input_name)
    out_file = os.path.join(path, "Outputs/lammps_out/",in_location,lammps_output_name)
    mpistr = "mpirun -n 1 lmp_beacon < "
    output_op = " > "
    sp.Popen(mpistr + in_file + output_op + out_file, shell=True).wait()
    os.replace(path+"/log.lammps", path+"/Outputs/lammps_out/" + in_location + '/' + log_name)
    
#Complete
def Optimizelattice(): 
    print('Minimization started!\n  Optimizing Lattice...')
    
    
    #Specifying lammps files to run for optimization
    lammps_input_name = 'Emin.lammps'
    in_location = 'E_min'
    lammps_output_name = 'lat_min.out'
    log_name = "Emin.log"
    
    #Running lammps with files
    runLammps(lammps_input_name,in_location,lammps_output_name,log_name)  
    #Converting Output into python variable
    lat_const = Lmps_txt2var('lat_const.txt')
    
    print("  Lattice Minimization @ 0 K Success!")
    return lat_const

#Complete, combine with other later
def Optimizelattice_finite(temps):    
    print('Finite Temp Optimization started!\n')
    import numpy as np
    
    lat_temp = np.zeros((len(temps),2),dtype=float)
    
    lammps_input_name = 'Emin_finite.lammps'
    in_location = 'E_min'
    lammps_output_name = 'lat_min_finite.out'
    log_name = 'lat_min_finite.log'
    
    count = 0
    for i in temps:
        print('  Running with Temperature of',i,'[K]')
        Var_txt(i,'lat_temp.txt')
        runLammps(lammps_input_name,in_location,lammps_output_name,log_name) 
        lat_temp[count,0] = Lmps_txt2var('fin_temp.txt')
        lat_temp[count,1] = Lmps_txt2var('lat_const_finite.txt')           
        count += 1
        
    print("  Lattice Optimization @ finite Temps Success!")
    return lat_temp

#could be done a lot cleaner, temp input determining the process
def Bulk_prop(lat_temp):
    import numpy as np
    lammps_input_name = "in.elastic"
    
    if lat_temp == 0:
        in_location = 'Bulk_prop'
        lammps_output_name = "bulk_0K.out"
        log_name = 'bulk_0K.log'
        runLammps(lammps_input_name,in_location,lammps_output_name,log_name) 
        Bulk_var = []
        with open("BulkProp_0K.txt") as f:
           for line in f:
               name, value = line.split("=")
               Bulk_var.append(float(value)) #[GPa]
        return Bulk_var
    else:
        #Navigate to other directory Probably, not sure what most efficient structure is
        in_location = 'Bulk_finite'
        lammps_output_name = "bulk_finite.out"
        log_name = 'bulk_finite.log'
        #create vector of all values from everything
        Var_txt(lat_temp,'temp.txt')
        runLammps(lammps_input_name,in_location,lammps_output_name,log_name) 
        Bulk_val = np.zeros((7),dtype=float)
        count = 0
        with open("BulkProp_finite.txt") as f:
           for line in f:
               name, value = line.split("=")
               Bulk_val[count] = float(value) #[GPa]
               count += 1
        return Bulk_val

#how does it this work?
def EV_curves():
    print('Energy/Volume Curve Calculation started!\n  Calculating E/V curves..')
    import numpy as np
    
    flist_in =  ['Ecalc_fcc.lammps','Ecalc_bcc.lammps','Ecalc_sc.lammps','Ecalc_hcp.lammps'] 
    flist_out =  ['Ecalc_fcc.out','Ecalc_bcc.out','Ecalc_sc.out','Ecalc_hcp.out']
    log_list = ['Ecalc_fcc.log','Ecalc_bcc.log','Ecalc_sc.log','Ecalc_hcp.log']
    in_location = 'EV_curve'
    
    
    lat_para = np.arange(2.2,6.0,0.01)
    Ev_curve = np.zeros((len(lat_para),5),dtype=float)
    count = 0
    for i in lat_para:
        Var_txt(i,'constant.txt')
        for file in range(0,len(flist_in)):
            #reduce hard coding
            runLammps(flist_in[file],in_location,flist_out[file],log_list[file]) 
        Ev_curve[count,0] = Lmps_txt2var('length.txt')
        Ev_curve[count,1] = Lmps_txt2var('ecoh_fcc.txt')
        Ev_curve[count,2] = Lmps_txt2var('ecoh_bcc.txt')
        Ev_curve[count,3] = Lmps_txt2var('ecoh_sc.txt')
        Ev_curve[count,4] = Lmps_txt2var('ecoh_hcp.txt')
        count += 1
    print('  E/V Curve Calculation Successful!')
    return Ev_curve
    
def Pt_defect_prop():   
    print('Point Defect Calculations started!\n  Calculating Point Defect Energies...')
    lammps_input_name = 'Vacancy.lammps'
    in_location = 'Point_def'
    lammps_output_name = 'V_def.out'
    log_name = 'V_def.log'
    
    runLammps(lammps_input_name,in_location,lammps_output_name,log_name)
    
    lammps_input_name = 'Interstitial.lammps'
    in_location = 'Point_def'
    log_name = 'I_def.log'
    
    runLammps(lammps_input_name,in_location,lammps_output_name,log_name)
    
    Vac_Energy = Lmps_txt2var('V_Energy.txt')
    Int_Energy = Lmps_txt2var('I_Energy.txt')
    print('  Point Defect Energy Calculation Successful!')
    return Vac_Energy,Int_Energy
    
def ThermExp_SpecificH(NPTstep, delta,lat_size,stable_structure,temp):
    print('Thermal Expansivity and Specific Heat Calculation Begun!\n  Calculating...')
    from Thermal import Thermal_calc,Specific_H
    import os
    path = os.getcwd()
    lammps_input_name = 'Thermal_exp.lammps'
    in_location = 'Thermal'
    lammps_output_name = 'Thermal_exp.out'
    log_name = 'Thermal_exp.log'
    
    Var_txt(delta, 'deltatemp.txt')
    Var_txt(NPTstep, 'timesteplength.txt')
    Var_txt(lat_size, 'lat_size.txt')
    Var_txt(temp,'temp.txt')
    
    runLammps(lammps_input_name,in_location,lammps_output_name,log_name)
    
    stepsize = 100
    Thermal_type = 'Exp'
    out_file = os.path.join(path, "Outputs/lammps_out/Thermal",lammps_output_name)
    Therm_exp = Thermal_calc(out_file,stepsize,NPTstep,delta,Thermal_type)
    
    #no switch statement in python bug here don't forget
    if stable_structure == 'fcc':
        atom_in_unit = 4;
    elif stable_structure == 'bcc':
        atom_in_unit = 2;
    elif stable_structure == 'sc':
        atom_in_unit = 1;
    elif stable_structure == 'hcp':
        atom_in_unit = 6;
    else:
        atom_in_unit = 4;
    sim_atoms = (lat_size ** 3) * atom_in_unit
    SpecificH = Specific_H(out_file,stepsize,NPTstep,delta,sim_atoms)
    print('Thermal Expansivity and Specific Heat Calculation Success!')
    return Therm_exp,SpecificH
    
def Iso_comp(NPTstep, delta,lat_size,pres):
    print('Isothermal Compressibility Calculation Begun!\n  Calculating...')
    from Thermal import Thermal_calc
    import os
    path = os.getcwd()
    lammps_input_name = 'Iso_comp.lammps'
    in_location = 'Thermal'
    lammps_output_name = 'Iso_comp.out'
    log_name = 'Iso_comp.log'
    
    Var_txt(delta, 'deltapres.txt')
    Var_txt(NPTstep, 'timesteplength.txt')
    Var_txt(lat_size, 'lat_size.txt')
    Var_txt(pres,'pres.txt')
    

    runLammps(lammps_input_name,in_location,lammps_output_name,log_name)
    
    stepsize = 100
    Thermal_type = 'Comp'
    
    out_file = os.path.join(path, "Outputs/lammps_out/Thermal",lammps_output_name)
    B = Thermal_calc(out_file,stepsize,NPTstep,delta,Thermal_type)
    print('Isothermal Compressibility Calculation Success!')
    return B
    
    
def Thermal_cond(temp):
    print('Thermal Conductivity Calculation Begun!\n  Calculating...')
    import os
    path = os.getcwd()
    lammps_input_name = 'kappa.heatflux'
    in_location = 'KAPPA'
    lammps_output_name = 'kappa.out'
    log_name = 'kappa.log'
    Var_txt(temp,'temp.txt')
    
    runLammps(lammps_input_name,in_location,lammps_output_name,log_name)
    Therm_cond = Lmps_txt2var('Therm_cond.txt')
    
    log_name = 'kappa_Autocorrelation.dat'
    os.replace(path+"/J0Jt.dat", path+"/Outputs/lammps_out/" + in_location + '/'+ log_name)
    print('Thermal Conductivity Calculation Success!')
    return Therm_cond
    
#def Melt_pt(lammps_input_name,lammps_output_name,lat_const):
    
#def Heat_Melt(lammps_input_name,lammps_output_name,lat_const):
    
def Lmps_txt2var(var_file):
    import os
    #implement other with this
    path = os.path.join(os.getcwd(),var_file)
    with open(var_file, 'r') as file:
        var = file.read().replace('\n', '')
    os.remove(path)    
    return var

#Create txt file with variable
def Var_txt(val,fname):
    
    global txt_list
    txt_list.add(fname)
    print(txt_list)
    file = open(fname, "w+")
    file.write(str(val)+' ')
    file.close()

def decorate(length):
    #Hopefully still works with different stdout
    for i in range(0,length):
            print('#',end = '')
    print()

def Read_input_file(file):
    with open(file, 'r') as f:    
        for line in f:
            if 'Interatomic' in line: 
                potential = f.readline()
            elif 'Potential' in line:
                pair_style = f.readline()
            elif 'Species' in line:
                Type = f.readline()
            elif 'Stable Structure' in line:
                stable_structure = f.readline()
            elif 'Initial Guess' in line:
                 lattice_guess = float(f.readline())
            elif 'Temperature Range' in line:
                temp_low,temp_high,temp_del = f.readline().split(",")
            elif 'Temperature Delta' in line:
                deltatemp = float(f.readline())
            elif 'Pressure Delta' in line:
                deltapres = float(f.readline())
            elif 'NPT Timesteps' in line:
                NPTstep = int(f.readline())
            elif 'Unit cells' in line:    
                lat_size = int(f.readline())
            elif 'Output file Name:' in line:
                fout_name = f.readline()
    return potential,pair_style,Type,stable_structure,lattice_guess,float(temp_low),float(temp_high),float(temp_del),deltatemp,deltapres,NPTstep,lat_size,fout_name

txt_list =  set()

if __name__ == '__main__':
    main()







