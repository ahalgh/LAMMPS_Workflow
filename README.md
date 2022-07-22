# LAMMPS_Workflow
Python Automation of LAMMPS Workflow, for automated testing of developed interatomic potentials
https://www.lammps.org/

Author: Alex Greenhalgh

Date: 5/30/2021

Contact: agreenh1@vols.utk.edu, (865) 456-1554
 

The MEAM_workflow directory determines various thermodynamic and structural properties of an interatomic potential file

MEAM_workflow structure:

Workflow_job calls the MEAM_prop.py python script, which takes care of calling all the lammps scripts and calculating 

the resulting values

### Repository Structure
```
/MEAM_workflow
 |
 +-- README.txt
 |    
 +-- Workflow_job: Job file to submit to HPC cluster, loads python and lammps, assigns envmental variable LAMMPS_POTENTIALS with location of Input_potential directory so potential can be found
 |     
 +-- Input_potential
 |  |  
 |  +-- User_input.txt: User inputs most stable phase, potential file name, etc
 |  +-- Potential_file: 'Al1_eam.fs' - generic test case
 |    
 +-- Python_automation
 |  |  
 |  +-- MEAM_properties.py: Main automation script, contains most of the modules
 |  +-- Pygraph.py: Graphing for Ev_curves, lattice optimization, and bulk properties, melting point graphing not incorporated yet
 |  +-- Thermal.py: Thermal Calculations, used for specific heat, isothermal compressibility, and Thermal expansivity
 |    
 +-- LAMMPS_scripts
 |  |  
 |  |-- Bulk_prop: Bulk properties at 0 K, From LAMMPS examples directory
 |  |-- Bulk_finite: Bulk properties at finite temps, From LAMMPS examples directory
 |  |-- E_min: Energy minimization and simulations, finite temps and 0K 
 |  |-- EV_curve: Energy Volume Curves, predicts most stable phase
 |  |-- H_melt: Heat of fusion, Not yet working
 |  |-- KAPPA: Thermal Conductivity, From LAMMPS examples directory
 |  |-- Melt_pt: Melting Point simulations, Not yet working
 |  |-- Point_def: Energy of Defect formation, from https://icme.hpc.msstate.edu/mediawiki/index.php/LAMMPS_Vacancy_Formation_Energy.html
 |  |-- Thermal: Simulations for Thermal Expansivity, Compressibility, and Specific Heat
 |    
 +-- Outputs
 |  |  
 |  |-- Graphs: Contains all the graphs from pygraphs
 |  |-- lammps_output: Same format as lammps scripts, containing .out and .log files from lammps scripts
```


### Example Output

#### Potential Energy Curves Graph
![Ev curve](/Outputs/Graphs/EV_Curves.png)

Workflow calculation of the potential energy curves of the Al1_eam.fs potential, FCC phase is the minimum energy phase, followed by HCP. In line with other theoretical and experimental [results](https://www.ctcms.nist.gov/potentials/entry/2008--Mendelev-M-I-Kramer-M-J-Becker-C-A-Asta-M--Al/EAM_Dynamo_MendelevKramerBecker_2008_Al__MO_106969701023_005.html). 

#### Elastic Constants over Temperature graph
![Elastic Curve](/Outputs/Graphs/Elastic.png)

Results confirmed by [potential paper](https://www.tandfonline.com/doi/abs/10.1080/14786430802206482)
```
Properties of  Al1.eam.fs Potential File:


Lattice minimization @ 0 [K]:
##############################
Lattice Constant:  4.04525979567614 
Took 0.2927 seconds, Total: 0.2927

Lattice Constant and Elastic Properties Over Temperature:

##################################################################################################################################################################################################################
 |   Temperature [K]    |  Lat Parameter [Å]   |  C11 Constant [GPa]  |  C12 Constant [GPa]  |  C44 Constant [GPa]  |  Bulk Modulus [GPa]  |  Shear Mod 1 [GPa]   |  Shear Mod 2 [GPa]   |    Poisson Ratio     | 
##################################################################################################################################################################################################################
 |       0.988816       |       4.045383       |      113.983634      |      62.541122       |      33.024655       |      79.688432       |      33.025045       |      25.722347       |       0.354285       | 
 |      299.882376      |       4.072969       |      111.834429      |      67.151127       |      36.718621       |      81.930444       |      36.876705       |      22.459545       |       0.374411       | 
 |      598.897613      |       4.103480       |      94.219676       |      60.903695       |      32.676751       |      72.295390       |      31.806312       |      16.858392       |       0.391815       | 
 |      933.051507      |       4.129543       |      65.459723       |      45.789491       |      22.579135       |      53.138101       |      22.416227       |       9.803909       |       0.413095       | 
 |     1177.098764      |       4.255623       |      33.892830       |      31.537863       |       2.086264       |      31.669588       |       1.712945       |       0.317374       |       0.495006       | 
 |     1522.332848      |       4.303088       |      29.006566       |      29.537245       |       2.453833       |      27.766444       |       1.512414       |       0.451758       |       0.491909       | 
##################################################################################################################################################################################################################

Took 671.0261 seconds, Total: 671.3189

Energies of Defect Formation:
##############################
Vacancy:  0.658443173931119 
Interstitial:  2.42449686762939 
Took 1.3389 seconds, Total: 916.6873

Thermal Properties:
##############################
Thermal Conductivity:  0.260390640372883 
Took 88.4994 seconds, Total: 1005.1866 seconds
Thermal Expansivity:  5.399676720440276e-05  [1/K]
Isothermal Compressibility:  1.3092424781487365e-06 [1/bar]
Specific Heat Capacity:  20.59811469658918  [J/mol*K]
Took 4.8566 seconds, Total: 1010.0433
```

This is an older version of the workflow, new version has various updates to structure and features but code will remain private to insure research integrity. Inflexible LAMMPS scripts replaced with all python.
