# NOTE: This script can be modified for different pair styles 
# See in.elastic for more info.

reset_timestep 0

# Choose potential
variable pairstyle file pairsty.txt
pair_style ${pairstyle} 
variable potential file potential.txt
variable type file type.txt
pair_coeff * * ${potential} ${type}

# Setup neighbor style
neighbor 1.0 nsq
neigh_modify once no every 1 delay 0 check yes

# Setup output

fix avp all ave/time  ${nevery} ${nrepeat} ${nfreq} c_thermo_press mode vector
thermo		${nthermo}
thermo_style custom step temp pe press f_avp[1] f_avp[2] f_avp[3] f_avp[4] f_avp[5] f_avp[6]
thermo_modify norm no

# Setup MD

timestep ${timestep}
fix 4 all nve
if "${thermostat} == 1" then &
   "fix 5 all langevin ${temp} ${temp} ${tdamp} ${seed}"


