# <span style="color: #0048d8">**extract_particles**</span>

### *summary*
---

Extract particles from a 2d image given a set of x,y coordinates. TODO link to info on the PLT format. (Should also add star file option if it isn't in the alpha version.)

### *cli options*
---

**none**

### *interactive options*
---

**micrograph_filename**					

+ The input micrograph, in which we will look for particles.

**coordinates_filename**				

+ The input particle coordinates, in Imagic-style PLT forlmat.

**output_stack_filename**				

+ Filename for output stack of particles.

**output_stack_box_size**				

+ Box size for output candidate particle images in pixels. Give 0 to skip writing particle images to disk.