# <span style="color: #0048d8">**sharpen_map**</span>

### *summary*
---

Sharpen a map by flattening the power spectrum of the high resolution Fourier amplitudes, optionally adding a b-factor. 

Can apply statistics calculated from calculate_fsc.

Optionally invert handedness of the map.

### *cli options*
---

**none**
### *interactive options*
---

**input_volume**	

+ Name of input image file.

**output_volume**	

+ Name of sharpened output volume.

**input_mask**		

+ Name of input image file.

**res_statistics**	

+ Input reconstruction statistics, The table listing FSC, Part_FSC, Part_SSNR and Rec_SSNR.

**use_statistics**		

+ Use statistics", "Answer No if no statistics are available?.

**pixel_size**		

+ Pixel size of the map in Angstroms.

**inner_mask_radius**	

+ Inner radius of mask to be applied to the input map, in Angstroms.

**outer_mask_radius**	

+ Outer radius of mask to be applied to the input map, in Angstroms.

**bfactor_low**		

+ B-factor to be applied to the non-flattened part of the amplitude spectrum, in Angstroms squared.

**bfactor_high**		

+ High-res B-Factor (A^2). B-factor to be applied to the flattened part of the amplitude spectrum, in Angstroms squared.

**bfactor_res_limit**	

+ Low resolution limit for spectral flattening (A). he resolution at which spectral flattening starts being applied, in Angstroms. (Default: 8.0)

**resolution_limit**	

+ High resolution limit (A). Resolution of low-pass filter applied to final output maps, in Angstroms. (Default: 3.0)

**filter_edge**		

+ Filter edge width (A). Cosine edge used with the low-pass filter, in Angstroms. (Default: 20.0)

**fudge_SSNR**		

+ Part_SSNR scale factor. Scale the Part_SSNR curve to account for disordered regions in the map. (Default: 1.0)

**use_mask**			

+ Should the 3D mask be used to mask the input map before sharpening?.

**invert_hand**		

+ Invert handedness. Should the map handedness be inverted?