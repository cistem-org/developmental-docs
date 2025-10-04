# <span style="color: #0048d8">**calculate_fsc**</span>

### *summary*
---

Calculate the solvent corrected FSC between two volumes. Output is a text file with the FSC, partFSC and SSNR values.

### *cli options*
---

**none**

### *interactive options*
---

**output_reconstruction_1**	 

The first input 3D reconstruction used for FSC calculation.

**output_reconstruction_2**

The second input 3D reconstruction used for FSC calculation.

**input_mask**					

Name of input 3D volume to be applied to input reconstructions. (optional)

**res_statistics**				

Output resolution statistics. The table listing FSC, Part_FSC, Part_SSNR and Rec_SSNR. (optional)

**pixel_size**					

Pixel size of the map in Angstroms.

**inner_mask_radius**				

Radius of a circular mask to be applied to the center of the input reconstructions, in Angstroms. (default: 0)

**outer_mask_radius**				

Radius of a circular mask to be applied to the input reconstructions, in Angstroms.

**molecular_mass_in_kDa**			

Total molecular mass of the particle to be reconstructed in kilo Daltons.

**use_mask**						

Should the 3D mask be used to mask the input reconstructions before FSC calculation?. (default: No)