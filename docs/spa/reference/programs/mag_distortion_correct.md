# <span style="color: #0048d8">**mag_distortion_correct**</span>

### *summary*
---

Correct images for magnification distortion.

### *cli options*
---

**none**

### *interactive options*
---

**input_filename** 

+ The input file, containing the images you want to correct.

**output_filename**

+ The output file, containing the distortion corrected images.

**mag_distortion_angle** 

+ The distortion angle in degrees. (default: 0.0)

**mag_distortion_major_scale** 

The major axis scale factor. (default: 1.0)

**mag_distortion_minor_scale** 

+ The minor axis scale factor. (default: 1.0)

**movie_is_gain_corrected** 

+ Are the input frames are already gain-corrected, if no, you can provide a gain to apply. (default: Yes)

````{panels}

```python
if (No):
```

---
	
**gain_filename**  

+ The filename of the camera's gain reference image.

````

**resample_output** 

+ Resample the output? If yes, the image will be resampled using Fourier cropping to the desired size. (default: No)

````{panels}

```python
if (Yes):
```	

---

**new_x_size**  

+ The desired X size after resampling. (allowed > 1)

**new_y_size**  

+ The desired Y size after resampling. (allowed > 1)

````