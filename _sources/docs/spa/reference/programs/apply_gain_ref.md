# <span style="color: #0048d8">**apply_gain_ref**</span>

### *summary*
---

Apply a gain reference, and optionally a dark reference, to a set of images. 

This program also can apply other statistical preprocessing, including:
 + removing outliers (based on a Gaussian distribution)
 + normalizing the image (by subtracting the mean and dividing by the standard deviation)

Finally, the pixel size (sampling rate) of the image may be changed by resizing. Here the, resizing is carried out in Fourier space, such that the new pixel size is given by:

```code
new_pixel_size = old_pixel_size * (old_size / new_size)
```

### *cli options*
---

**none**

### *interactive options*
---

**input_filename**	

 - Filename of input image

**output_filename**			

 - Filename of output image

**input_gain_filename**		

 - Filename of gain reference

**also_use_dark** 

 - Also do dark correction? If yes, you can provide a dark image to be subtracted:

````{panels}

```python
if (Yes)
```

---

**input_dark_filename**			

+ Filename of dark reference.

````


	
**should_resample**        

 - Resample the output? If yes, you can resample the output to a different size

````{panels}

```python
if (Yes)
```

---


**new_x_size**         

+ Wanted New X-Size. The image will be Fourier cropped to this size


**new_y_size**                 

+ Wanted New Y-Size. The image will be Fourier cropped to this size

````

**should_remove_outliers**    

 - Remove outlier pixels? If yes, outlier pixels will be removed AFTER gain correction, but prior to resampling
 
````{panels}

```python
if (Yes)
```

---


**num_sigmas**		

- Pixels more than this number of standard deviations above or below the mean will be reset to the mean
````

**zero_float_and_normalize**	

 - After outlier pixels have been removed, zero-float and normalize images

