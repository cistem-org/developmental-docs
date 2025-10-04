# <span style="color: #0048d8">**resize**</span>

### *summary*
---

Change the box size of an image or volume, optionally normalizing the densities as well.

```{note}
Does not alter the pixel size.
```

### *cli options*
---

**none**

### *interactive options*
---

**input_filename**		

+ Filename of input image.

**output_filename**	

+ Filename of output image.

**is_a_volume**         

Is the input a volume? Yes if it is a 3D.

**new_x_size**          

+ Wanted new X size.

**new_y_size**          

+ Wanted new Y size.

**new_z_size**

+ Wanted new Z size.
            	
**should_normalise**    

+ If yes, images will also be normalized and zero floated.
