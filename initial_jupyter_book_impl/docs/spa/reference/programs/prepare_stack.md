# <span style="color: #0048d8">**prepare_stack**</span>

### *summary*
---

Takes a stack of 2d particles, estimates the background noise powerspectrum, then applies this to whiten the noise in the particle images as well as setting the mean and variance to 0, and 1 respectively.

### *cli options*
---

**none**

### *interactive options*
---


**input_particle_images** 

+ The input image stack, containing the experimental particle images.

**input_star_file**
 
+ Input cisTEM star file. The input parameter file, containing your particle parameters.

**output_particle_images** 

+ The output image stack, containing the prepared particle images.

**pixel_size** 

+ Wanted Output Pixel Size (Angstroms).

**mask_radius** 

+ Mask radius (Angstroms), for calculating noise statistics. (default: 100)

**resample_box**

+ Resample output? If yes you can resample the output image to a specified size. (default: No)

````{panels}

```python
if (Yes):
```

---
  
**wanted_output_box_size** 

+ Resampled box size: How big to resample the box size to?. (default: 512)
	
````