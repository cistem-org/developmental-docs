# <span style="color: #0048d8">**apply_mask**</span>

### *summary*
---

2d && 3d images.

Apply a supplied mask that may optionally be smoothed. Values outside the mask may be set to a constant, or low-pass filtered.

### *cli options*
---

**none**

### *interactive options*
---

**input_volume**	

+ Name of input image file.

**input_mask**		

+ Name of input image (mask) file.

**output_volume**	

+ Name of the output masked image/volume file name.

**pixel_size**		

+ Pixel size of input images in Angstroms.

**cosine_edge**		

+ Width of cosine edge (A). Width of the smooth edge to add to the mask in Angstroms. (default: 10.0)

**outside_weight**	

+ Weight of density outside mask. Factor to multiply density outside of the mask. (default: 0.0)

**filter_radius**		

+ Low-pass filter to be applied to the density outside the mask. (default: 0.0)

**outside_value**		

+ Value used to set density outside the mask. (default: 0.0)

**use_outside_value**  

+ Should the density outside the mask be set to the user-provided value. (default: No)