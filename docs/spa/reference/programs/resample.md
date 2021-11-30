# <span style="color: #0048d8">**resample**</span>

### *summary*
---

Changes the **pixel size** of a volume based on the change in size.

```code
new_pixel_size = old_pixel_size * (old_size / new_size)
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
  
+ Is the input a volume? Yes if it is a 3D. (default: No)

**new_x_size**
  
+ Wanted new X size.

**new_y_size**         

+ Wanted new Y size.


**new_z_size**          

+ Wanted new Z size.

	