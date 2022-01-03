#/bin/bash


# Specify where your alphas version of cisTEM is installed. 
path_to_cistem="${HOME}/cisTEM_alpha/src"

# Singulatiry can be run with "singularity shell" to give you an "interactive" env in the container.
# In this example, we instead execute a specific function in the container
function_to_execute="simulate"

# If you are running match_template, you need the --nv flag as below, if the flag is included and the machine has no gpus, it will not run.
# Singularity will bind your homedirectory, and should bind the PWD. Outside of this, it will not know about your filesystem
# If you want to give access (say your images are on nrs or a scratch disc somewhere, add the --bind directive.

#singularity exec --nv --bind /scratch_dublin/himesb /groups/himesb/notes/cisTEM_20210401 /cisTEM/bin/simulate

################################
# File things
################################
output_filename="betgal_vacuum.mrc"
input_pdb_file="bgal_flat.pdb" # the parser is fairly good with PDB format, but will probably break in some cases.
output_size=-320 # pixels - if < 0 a hack to set a fixed size for 2d image simulation, if > 0 the size of a 3D reference volume to simulate.
n_threads=16 # Not so important for a a 3d, it will be fast either way.


################################
# Bluring things
################################
linear_scaling_of_PDB_bfactors=1.0 # make sure your model is reasonable i.e. the builder didn't set all bfactors to 50 or something. can be between 0 and 1
per_atom_bfactor=4.0 # add any bfactor to all atoms, may need to be increased since motion is not considered in the 3d simulation

################################
# Imaging things
################################
pixel_size=1.0
CS=2.7 # mm
KV=300 # kev
OA=100 # micron, objective aperture won't affect a 3D sim

wanted_defocus=8000 # Angstrom
minimum_thickness=10

exposure_per_frame=1.5 # e-/Ang^2 ;; Dose rate doesn't affect 3D sim (only 2d) here it is used with n_frames to get the total exposure
exposure_rate=3.0 # e-/ pixel /s
n_frames=1
pre_exposure=0 # If you've left off some early frames, account for that here
n_particles=1

water_scaling=0.0 # Linear scaling of water molecules - normally not used, except for demonstration purposes


################################
# Don't worry about things
################################
# There are some options that I plan to set as default, but due to the way things are written, need to be passed via command line args.
from_future_args=" --only-modify-signal-3d=2 --wgt=0.225 --water-shell-only"

################################
# Optional things
################################
# --save-detector-wavefunction : this is the probability distribution (really the square complex modulus of the detector wavefunction)
# --skip-random-angles : when simulating a particle stack, the orientation is randomized. For this tutorial, we want a consistent view to compare different conditions
# --max_number_of_noise_particles=6

optional_args=" --save-detector-wavefunction --skip-random-angles "

################################
# Run the thing
################################

${path_to_cistem}/${function_to_execute} ${from_future_args} ${optional_args} << EOF
$output_filename
$output_size
$n_threads
$input_pdb_file
no
$pixel_size
$linear_scaling_of_PDB_bfactors
$per_atom_bfactor
no
$n_particles
$wanted_defocus
0
$exposure_per_frame
$exposure_rate
$n_frames
yes
no
$water_scaling
0.0
$KV
$OA
$CS
0.0
$pre_exposure
32
$minimum_thickness
5
0.0
2.0
0.1
0.0001
0.0
0.0
0.0
0.0
EOF




