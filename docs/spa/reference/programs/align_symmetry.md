# <span style="color: #0048d8">**align_symmetry**</span>

### *summary*
---

This program attempts to align an unsymmetryized volume to a symmetry axes that corresponds to the definitions used in *cis*TEM. 

### *cli options*
---

**none**

### *interactive options*
---

**input_volume_file**
 - filename, The volume you want to align

**wanted_symmetry**
 - string, Symmetry to align to, e.g. "C2"

**output_volume_file_no_sym**
 - filename, The volume that has been aligned, but not symmetrized

**output_volume_file_with_sym**
 - filename, The volume that has been aligned and symmetrised

**initial_angular_step** 
 - float, Initial angular search step in degrees, default 5.0.