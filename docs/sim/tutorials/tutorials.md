# <span style="color: darkgreen">***Tutorials***</span>


(seeAbove1)= 
## 1 - Get an alpha version of *cis*TEM

To run the simulator or template matching you will need an alpha version of *cis*TEM. For most people, the best choice will be to download a pre-compiled binary, following the instuctions here: [get cistem tutorial](get_cistem.md) For those interested in compiling form source code, you will need to add the "--enable-experimental" flag to your configure line, as well as following the instructions [here.](https://github.com/bHimes/cisTEM_downstream_bah/wiki/Compiling-cisTEM)



## 2 - Calculate a 3D scattering potential

Simulation in TEM involves describing

1) The Coulomb potential of the sample
2) The relativistic wave function of the imaging electrons
3) The interaction of 1 & 2
4) The influence of the microscope optics, including the lenses, detectors etc.

Step one is also the first step in a template matching experiment, were the detection efficiency is directly tied to the output SNR from the matched filter used in 2DTM. The SNR in turn depends strongly on how well your calculated specimen potential matches the imaged specimen potential recorded in your micrographs(s). To improve detection, both points 1 & 4 from above need to be carefully handled. 


### Materials needed
* An alpha version of *cis*TEM [see above.](seeAbove1)
* Information about the imaging conditions used in the data you wish to search.
* A PDB representing your molecule
```{warning}
Only classic [PDB format](https://en.wikipedia.org/wiki/Protein_Data_Bank_(file_format)) is supported at the moment. Support for newer PDBx/mmCIF is planned, but in the interm, you will need to manually convert to PDB using a tool like Chimera for example. Simply open your mmCIF and then "save as PDB."
```

After gathering the required materials, you may adapt [the following script](../../TM/tutorials/make_3d_ref.md) to your specific use case.

## 3 - Calculate a stack of noisy particles

**Under construction**

% TODO:




