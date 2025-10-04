# <span style="color: #0048d8">**sum_all_tif_files**</span>
### *summary*
---

Create a gain and dark reference computed from a set of tiff files. All tiff files in this directory must be the same size.

### *cli options*
---

**none**
### *interactive options*
---


**output_filename**		

+ Filename of output image.

**make_dark_and_gain**			

+ Estimate Dark and Gain images. If yes, a dark and gain image will be estimated.

````{panels}

```python
if (Yes)
```

---


**output_dark_filename**		

+ Filename of output dark image.

**output_gain_filename**		

+ Filename of output gain image.

````

**max_threads**

+ Maximum number of threads to use for processing.
