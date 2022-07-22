# LAMMPS_Workflow
Python Automation of LAMMPS Workflow, for automated testing of developed interatomic potentials
https://www.lammps.org/

This is an older version of the workflow, new version has various updates to structure and features but code will remain private


Author: Alex Greenhalgh
Date: 5/30/2021
Contact: agreenh1@vols.utk.edu, (865)456-1554
 

The MEAM_workflow directory determines various thermodynamic and structural properties of an interatomic potential file

MEAM_workflow structure:
Workflow_job calls the MEAM_prop.py python script, which takes care of calling all the lammps scripts and calculating 
the resulting values


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
