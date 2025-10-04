# <span style="color: #0048d8">**scale_with_mask**</span>

### *summary*
---

Rescale the Fourier amplitude to match the (1d rotational average) of the Fourier amplitude of a reference volume.

This allows for a more accurate comparision of maps in real-space, within the limits of amplifying noise in either map.

### *cli options*
---

**none**

### *interactive options*
---

**input_ref_filename**				

+ Filename of volume to scale to.

**input_volume_filename**		

+ Filename of volume to scale.

**input_first_mask_filename**		

+ Input mask for volume #1. Filename of volume to use as a mask prior to calculating scale filter.

**input_second_mask_filename**		

+ Input mask for volume #2 (can be same). Filename of volume to use as a mask prior to calculating scale filter.

**output_filename**				

+ Filename of output scaled volume.

**apply_resolution_cut_off**         

+ Cut-Off Resolution?. If yes, the resolution will be cut off by a cosine at the specified resolution. (Default: No)


**pixel_size**                             

+ The pixel size in angstroms.

**resolution_cut_off**                     

+ Wanted resolution cut-off (A).
