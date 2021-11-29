# <span style="color: #0048d8">**apply_gain_ref**</span>

### *summary*
---


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

    **input_dark_filename**			

     - Input dark ref file", "Filename of dark reference", "dark.mrc", true );
	
**should_resample**        

 - Resample the output? If yes, you can resample the output to a different size

    **new_x_size**         

     - Wanted New X-Size. The image will be Fourier cropped to this size

		**new_y_size**                 

     - Wanted New Y-Size. The image will be Fourier cropped to this size

**should_remove_outliers**    

 - Remove outlier pixels? If yes, outlier pixels will be removed AFTER gain correction, but prior to resa

		**num_sigmas**		

     - Pixels more than this number of standard deviations above or below the mean will be reset to the mean

**zero_float_and_normalize**	

 - After outlier pixels have been removed, zero-float and normalize images

