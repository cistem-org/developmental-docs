# <span style="color: #0048d8">**estimate_dataset_ssnr**</span>

### *summary*
---

Estimate the spectral signal-to-noise ratio (SSNR) of a dataset.

### *cli options*
---

**none**

### *interactive options*
---


**input_filename**		

+ Filename of input particle stack to estimate.

**output_filename**		

+ Filename of output SSNR curve.

**defocus_filename**    

+ Text file with defocus values for each particle.

**pixel_size**             

+ The pixel size in Angstroms.

**acceleration_voltage**      

+ Acceleration voltage, in keV. (default: 300, allowed 0-500)

**spherical_aberration**    

+ Objective lens spherical aberration (mm). (default: 2.7)

**amplitude_contrast**    
   
+ Fraction of total contrast attributed to amplitude contrast. (default: 0.07

**number_of_ctf_rotations**    

+ The number of directions to sample to take astigmatism into account. (default: 18, allowed > 1)
 
**molecular_mass_in_kda**

+ The molecular weight of the sample.
