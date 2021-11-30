# <span style="color: #0048d8">**project3d**</span>

### *summary*
---

Create a stack of 2d projections at either random angles or from angles and shifts (optionally CTF applied) provided in a star file. 

Optionally adds Gaussian noise to a specified SNR.

### *cli options*
---


### *interactive options*
---

**input_reconstruction** 

The 3D reconstruction from which projections are calculated.

**project_based_on_star**

+ Angles from input .star file? If yes, angles and shifts will be obtained from an input star file, if not they will be made on a grid.

````{panels}

```python
if (Yes):
```

---

**input_star_filename**

+ Input cisTEM star filename. The input parameter file, containing your particle alignment parameters.

**first_particle**

+ The first particle in the stack for which a projection should be calculated.

**last_particle**

+ The last particle in the stack for which a projection should be calculated.

**apply_CTF**

+ Should the CTF be applied to the output projections? (default: No)

**apply_shifts**

+ Should the particle translations be applied to the output projections?" (default: No)

````

````{panels}

```python
else:
```

---

**angular_step**

+ Angular step size for grid projection.

````


**ouput_projection_stack**

+ The output image stack, containing the 2D projections.

**pixel_size**

+ Pixel size of input images in Angstroms.

**mask_radius**

+ Radius of a circular mask to be applied to the final reconstruction in Angstroms.

**wanted_SNR**

+ Wanted SNR. The ratio of signal to noise variance after adding Gaussian noise and before masking.

**padding**

+ Padding factor. Factor determining how much the input volume is padded to improve projections.

**my_symmetry**

+ The assumed symmetry of the particle to be reconstructed.

**apply_mask**

+ Should the particles be masked with the circular mask?

**add_noise**

+ Should the Gaussian noise be added?

**max_threads**

+ Max. threads to use for calculation.
