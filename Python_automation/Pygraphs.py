#Graphing all graphing modules for MEAM_properties.py

#Function for graphing Energy volume curves
def Ev_graph(Ev_mat):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import math as m
    import os
    path = os.getcwd()


    #def main():
    Length = Ev_mat[:, 0]
    fcc = Ev_mat[:, 1]
    bcc = Ev_mat[:, 2]
    sc = Ev_mat[:, 3]
    hcp = Ev_mat[:, 4]
    
    # Need to shorten length
    unit_cells = 7
    
    # Finding all Energy min and index of value for location
    minElement_fcc = np.amin(fcc)
    min_element = minElement_fcc
    
    #Finding location of each min element
    result = np.where(fcc == minElement_fcc)
    fcc_loc = int(result[0])
    min_loc = fcc_loc
    # print(fcc_lat,minElement_fcc,'\n')
    
    minElement_bcc = np.amin(bcc)
    result = np.where(bcc == minElement_bcc)
    bcc_loc = int(result[0])
    # print(bcc_lat,minElement,'\n')
    if minElement_bcc < min_element:
        min_element = minElement_bcc
        min_loc = bcc_loc

    minElement_sc = np.amin(sc)
    result = np.where(sc == minElement_sc)
    sc_loc = int(result[0])
    # print(sc_lat,minElement,'\n')
    if minElement_sc < min_element:
        min_element = minElement_sc
        min_loc = sc_loc

    
    minElement_hcp = np.amin(hcp)
    result = np.where(hcp == minElement_hcp)
    hcp_loc = int(result[0])
    # print(hcp_lat,minElement,'\n')
    if minElement_bcc < min_element:
        min_element = minElement_hcp
        min_loc = hcp_loc

    #V_int = fcc_lat^3
    
    # Now need to calculate delE for variety of lattices
    Energy_arr = [fcc[fcc_loc], bcc[bcc_loc], sc[sc_loc], hcp[hcp_loc]]
    
    min_struct = Length[min_loc]/unit_cells
    print(Energy_arr, min_struct,min_element)
    #massive cohesive energy if lattice constant is too large, only graphing important part
    del_graph = int(len(Ev_mat) / 15)
    
    # Just formatting for easy graphing, scale of energy values jumps extremely high outside of
    # ~.50 Angstroms of ideal lattice constant, making sure only graphing the important part
    fcc_E = fcc[fcc_loc-del_graph:fcc_loc+del_graph]
    fcc_Length = Length[fcc_loc-del_graph:fcc_loc+del_graph]
    fcc_Length = fcc_Length/unit_cells
    
    bcc_E = bcc[bcc_loc-del_graph:bcc_loc+del_graph]
    bcc_Length = Length[bcc_loc-del_graph:bcc_loc+del_graph]
    bcc_Length = bcc_Length/unit_cells
    
    sc_E = sc[sc_loc-del_graph:sc_loc+del_graph]
    sc_Length = Length[sc_loc-del_graph:sc_loc+del_graph]
    sc_Length = sc_Length/unit_cells
    
    hcp_E = hcp[hcp_loc-del_graph:hcp_loc+del_graph]
    hcp_Length = Length[hcp_loc-del_graph:hcp_loc+del_graph]
    hcp_Length = hcp_Length/unit_cells
    
    # For loop to calculate V/V0_stable_phase and delE_stable_phase
    for i in range(0, len(fcc_Length)):
        frac_fcc = (fcc_Length ** 3 / 4) / (min_struct ** 3/4)
        fcc_Edel = fcc_E - min_element
        frac_bcc = (bcc_Length ** 3 / 2) / (min_struct ** 3/4)
        bcc_Edel = bcc_E - min_element
        frac_sc = (sc_Length ** 3 / 1) / (min_struct ** 3 / 4)
        sc_Edel = sc_E - min_element
        frac_hcp = (hcp_Length ** 3)*(m.sqrt(3) * m.sqrt(8/3)) / \
            4 / (min_struct ** 3 / 4)
        hcp_Edel = hcp_E - min_element
    
    # Plotting the Ev_curves
    out_file = os.path.join(path, "Outputs/Graphs/Ev_curve.png")
    plt.plot(frac_fcc, fcc_Edel)
    plt.plot(frac_bcc, bcc_Edel)
    plt.plot(frac_sc, sc_Edel)
    plt.plot(frac_hcp, hcp_Edel)
    plt.legend(['FCC', 'BCC', 'SC', 'HCP'])
    #Need to make graph labels not hard coded
    plt.xlabel('V/V0_fcc')
    plt.ylabel('DelE [eV]')
    plt.title('Potential Crystal Structure Stability')
    plt.grid()
    plt.savefig(out_file)

#Function for graphing Bulk properties with respect to temperature
def Bulk_graph(bulk_finite):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import os
    path = os.getcwd()
    #Loading in values from bulk value matrix
    Temp = bulk_finite[0,:]
    C11 = bulk_finite[1,:]
    C12 = bulk_finite[2,:]
    C44 = bulk_finite[3,:]
    Bulk_mod = bulk_finite[4,:]
    Shear_mod1 = bulk_finite[5,:]
    Shear_mod2 = bulk_finite[6,:]
    Poisson_R = bulk_finite[7,:]
    
    
    #Plotting figure 1, Elastic Constants of Potential with respect to temperature
    plt.figure(0)
    out_file = os.path.join(path, "Outputs/Graphs/Elastic_finiteT.png")
    plt.plot(Temp, C11)
    plt.plot(Temp, C12)
    plt.plot(Temp, C44)
    plt.legend(['C11', 'C12', 'C44'])
    plt.xlabel('Temperature [K]')
    plt.ylabel('Elastic constants [GPa]')
    plt.title('Elastic Constant of Al1 over Temperature')
    plt.grid()
    plt.savefig(out_file)
    
    #Plotting figure 2, Bulk and shear modulus of Potential with respect to temperature
    plt.figure(1)
    out_file = os.path.join(path, "Outputs/Graphs/Bulk_finiteT.png")
    plt.plot(Temp, Bulk_mod)
    plt.plot(Temp, Shear_mod1)
    plt.plot(Temp, Shear_mod2)
    plt.legend(['Bulk Modulus', 'Shear Modulus 1', 'Shear Modulus 2'])
    plt.xlabel('Temperature [K]')
    plt.ylabel('Elastic Properties [GPa]')
    plt.title('Elastic Properties of Al1 over Temperature')
    plt.grid()
    plt.savefig(out_file)
    
    #Plotting figure 2, Poisson_R_ of Potential with respect to temperature   
    plt.figure(2)
    out_file = os.path.join(path, "Outputs/Graphs/Poisson_R_finiteT.png")
    plt.plot(Temp, Poisson_R)
    plt.legend(['Poisson Ratio'])
    plt.xlabel('Temperature [K]')
    plt.ylabel('Poisson Ratio')
    plt.title('Poisson Ratio of Al1 over Temperature')
    plt.grid()
    plt.savefig(out_file)

#Function for graphin graphing the lattice constant with respect to temperature    
def Finite_graph(lat_temp):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import os
    path = os.getcwd()
    
    #Loading matrix into variables
    Temp = lat_temp[:,0]
    lat = lat_temp[:,1]

    #Graphing optimal lattice constant with respect to temperature
    out_file = os.path.join(path, "Outputs/Graphs/lat_finite.png")
    plt.plot(Temp, lat)
    plt.ylabel('Equilibrated Lattice constant [A]')
    plt.xlabel('Temperature [K]')
    plt.title('Lattice Constant of Al1 over Temperature')
    plt.grid()
    plt.savefig(out_file)    
