# <span style="color: #0048d8">**applyctf**</span>

### *summary*
---

Apply one of three CTF correction methods to a stack of images.

1. Apply a simple phase flip that leaves the amplitudes unmodulated.
2. Apply the CTF via multiplication, which damps noise near the CTF zeros.
3. Apply a low-resolution boosting Wiener filter that produces images with contrast similar to a phase plate image. Based of the filter suggested by Dimitry Tegunove [link to repo] and also as implemented in emClarity as the "phakePhasePlate" option. [link to repo]

```{note}
The Wiener filter is only available in the newer alpha versions.
```

### *cli options*
---

**none**

### *interactive options*
---

**input_filename** 

+ The input file, containing one or more images in a stack.

**output_filename**

+ The output file.

**pixel_size** 

+ Pixel size of input images in Angstroms.

**acceleration_voltage** 

+ Acceleration voltage, in keV.

**spherical_aberration** 

+ Objective lens spherical aberration in mm.

**amplitude_contrast**

+ Fraction of total contrast attributed to amplitude contrast.

**input_ctf_values_from_text_file** 

+ Use a text file to input defocus values? If yes, a text file with one line per image is required

````{panels}

```python
if (yes):
```

---

**text_filename** 

- File containing defocus values, should have 3 or 4 values per line. 
  + defocus_1, defocus_2, astigmatism angle, (optionally) additional phase shift.
	
````

````{panels}

```python
else:
```
---

  **defocus_1**

  - The objective lens underfocus along the first axis.

  **defocus_2** 
  
  - The objective lens underfocus along the second axis.

  **astigmatism_angle**

  - Angle between the first axis and the x axis of the image.

  **additional_phase_shift** 

  - Additional phase shift relative to undiffracted beam, as introduced for example by a phase plate/

````	

**phase_flip_only**

+ Phase Flip Only. If Yes, only phase flipping is performed.

````{panels}

```python
if (NO):
```
----

Either, multiply by the CTF or apply a CTF with low-frequency Wiener filter depending on the answer to the next prompt.

````

**apply_wiener_filter** 

Apply Wiener Filter. If Yes, apply Wiener filter as suggested by Dimitry Tegunov.

````{panels}

```python
if (yes):
```

---

**wiener_filter_falloff_frequency**

+ SSNR Falloff frequency. In Angstromsm, the frequency at which SSNR falls off. (default = 100.0)

**wiener_filter_falloff_fudge_factor** 

SSNR Falloff speed. How fast does SSNR fall off. (default = 1.0)

**wiener_filter_scale_fudge_factor** 

Deconvolution strength. Strength of the deconvolution. (default = 1.0)

**wiener_filter_high_pass_radius** 

Highpass filter frequency. In Angstromsm, the frequency at which to cutoff low freq signal. (default = 200.0)

````


````{panels}

```python
else:
```
----

Simple CTF multiplication


````

**maintain_image_contrast** 

+ Maintain image contrast. If Yes, contrast is the same as image.

