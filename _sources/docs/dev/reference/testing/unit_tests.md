# *Unit Tests*

```{todo} Create and link dep methods.
For all methods in Functions Tested and Depends on below, create the corresponding entries in reference/classes and replace text with link.
```

# TestMRCFunctions

## Functionality Tested:

- Open a file with .mrc extension
- Check if the file is a valid MRC file
- Read and store the header information
- Read and store the image data

```{note}
  - This only tests the original reading of data from MRC mode (TODO: list) and storing as 32 bit float.
  - Aside from the raw data stream, this also adds/removes padding for in place FFTs which is not currently tested
```

## Depends on:

- MRCFile::OpenFile
- MRCFile::ReadSlice
- Artifact: hiv_images_80x80x10
---

# TestAssignmentOperatorsAndFunctions

## Functionality Tested:

- Copy an Image object and it's data into this Image, when the memory for this Image is not allocated.
- Copy an Image object and it's data into this Image, when the memory for this Image is allocated, and is a different size, such that it must first be deallocated.
- Call the Image::CopyFrom method, which just invokes the operator 
```c++
Image & Image::operator = (const Image *other_image)
```
- Assign by reference, which then also invokes the same operator as CopyFrom:
```c++
Image & Image::operator = (const Image &other_image)
{
	*this = &other_image;
	return *this;
}
```
- Unlike the previous tests, the Image::Consume method directly steals the memory pointed to by the other image.

## Depends on:

- Image::Allocate

```{warning}
  The Allocate method is not currently tested and does some fairly complicated things:
  - Mutex lock for FFT plan generation
  - Allocating memory including the proper padding
  - Asserting data memory is not currently allocated, and calling Image::Deallocate if needed
  - No asserts in place to confirm proper memory alignment either.
```

---
# TestFFTFunctions

## Functionality Tested:

  ```{warning}
    - We really only every use the MKL routines so FFTW3 is not tested nearly so well.
    - Because FFTW3 is GPL3 the FFTW3 routines need to be replaced with the equivalent MKL calls to be compatible with the current cisTEM license. Right now, they effectively only serve as a placeholder so the MKL knows where to wrap in their own routines, however, to be thorough, these should be
  ```

- Image::ForwardFFT
  - Inplace, single precision R2C using either FFTW3 or Intel MKL
- Image::BackwardFFT
- RemoveFFTWPadding

## Depends on:

- MRCFile::OpenFile
- MRCFile::ReadSlice
- Image::SetToConstant
- Artifact: sine_wave_128x128x1

---
(scaling-and-sizing-label)=
# TestScalingAndSizingFunctions

## Functionality Tested:

- Image::ClipInto

  - test real space clipping into a larger image.
  - test real space clipping into a smaller image.
  - test Fourier space clipping into a larger image.
  - test Fourier space clipping into a smaller image.
  - test real space clipping smaller to odd
  - test fourier space flipping smaller to odd


- Image::Resize

  - Real space big
  - Real space small
  - Fourier space big
  - Fourier space small

## Depends on:

- MRCFile::OpenFile
- MRCFile::ReadSlice
- Image::ForwardFFT
- Image::Consume
  - Tested in "Memory Assignment Ops and Funcs"

---
# TestFilterFunctions

## Functionality Tested:

- Image::ApplyBFactor

## Depends on:

- MRCFile::OpenFile
- MRCFile::ReadSlice
- Image::ForwardFFT
- Image::BackwardFFT

---
# TestAlignmentFunctions

## Functionality Tested:

- Image::PhaseShift
- Image::CalculateCrossCorrelationImageWith
- Image::FindPeakWithIntegerCoordinates
- Image::FindPeakWithParabolaFit

```{TODO} Add test for SwapRealSpaceQuadrants
  CalculateCrossCorrelationImageWith depends on SwapRealSpaceQuadrants, which depends on PhaseShift. TODO: SwapRealSpaceQuadrants is not currently tested.
```


## Depends on:

- MRCFile::OpenFile
- MRCFile::ReadSlice
- Image::ForwardFFT
- Image::BackwardFFT

---
# TestImageArithmeticFunctions

## Functionality Tested:

- Image::AddImage
- Image::SetToConstant

```{TODO} Add tests for these other arithmetic functions
- Image::SubtractImage
- Image::SubtractSquaredImage
- Image::MakeAbsolute
- Image::MultiplyPixelWiseReal
- Image::MultiplyPixelWise
- Image::ConjugateMultiplyPixelWise
- Image::DividePixelWise
```

## Depends on:
---
# TestSpectrumBoxConvolution

## Functionality Tested:

- Image::SpectrumBoxConvolution

## Depends on:

- MRCFile::OpenFile
- MRCFile::ReadSlice
- Image::ForwardFFT
- Image::BackwardFFT
- Artifact: hiv_image_80x80x1_filename

---
# TestImageLoopingAndAddressing

## Functionality Tested:

- Image::LoopingAndAddressing

## Depends on:

- None

---
# TestNumericTextFiles

## Functionality Tested:

- NumericTextFile::Init
- NumericTextFile::ReadLine
- NumericTextFile::WriteLine


## Depends on:

- none

---
# TestClipIntoFourier

## Functionality Tested:

- test Fourier space clipping into a larger image.
  - I think this tests redundant functionality, albeit with a different approach from the other clip into tests [TestScalingAndSizingFunction](scaling-and-sizing-label), TODO: verify
- test with odd dimensions into even dimensions
- test with even dimensions into odd dimensions
  - I think these tests are unique compared to [TestScalingAndSizingFunction](scaling-and-sizing-label)

## Depends on:

- MRCFile::OpenFile
- MRCFile::ReadSlice
- Image::ForwardFFT
- Image::BackwardFFT
- Image::SetToConstant
- Image::CopyFrom

```{warning}
Depends on currently untested methods.
- Image::AddGaussianNoise // TODO: Swap this for the STD functions and note that dependency.
- Image::ComputeAmplitudeSpectrum
```

---

# TestMaskCentralCross

## Functionality Tested:

- Image::MaskCentralCross

## Depends on:

- Image::SetToConstant

---
# TestStarToBinaryFileConversion

## Functionality Tested:

- cisTEMParameters::cisTEMParameters
- cisTEMParameterLine::cisTEMParemeterLine
- cisTEMParameters::parameters_to_write::SetAllToTrue
- cisTEMParameters::WriteTocisTEMStarFile
- cisTEMParameters::WriteTocisTEMBinaryFile
- cisTEMParameters::ClearAll
- cisTEMParameters::ReadFromcisTEMBinaryFile
- cisTEMParameters::ReturnFileSizeInBytes


## Depends on:

- wxFileName::GetTempDir(); 
- Return value from cisTEMParameters::WriteTocisTEMStarFile so the line with cisTEM version and datetime is ignored
  ```c++
    - int header_bytes_to_ignore = cisTEMParameters.WriteTocisTEMStarFile(star_from_binary_filename.ToStdString().c_str());
  ```
---

# TestElectronExposureFilter

## Functionality Tested:

- ElectronDose::CalculateDoseFilterAs1DArray


## Depends on:

```{warning}
- ZeroFloatArray is not currently tested.
```

---
# TestEmpiricalDistribution

## Functionality Tested:

- Image::ReturnDistributionOfRealValues
- EmpiricalDistribution::GetSampleMean
- EmpiricalDistribution::GetSampleVariance
- EmpiricalDistribution::GetMinimum
- EmpiricalDistribution::GetMaximum
- EmpiricalDistribution::GetSampleSumOfSquares


## Depends on:

- MRCFile::OpenFile 
- MRCFile::ReadSlice
- Artifact: hiv_image_80x80x1
---
# TestSumOfSquaresFourierAndFFTNormalization

## Functionality Tested:


- Image::ReturnSumOfSquares
  - In Fourier space without any DFT normalization. 
  - In Fourier space with DFT normalization after the forward transform.

## Depends on:

- MRCFile::OpenFile
- MRCFile::ReadSlice
- Image::ForwardFFT
- Image::BackwardFFT
- Artifact: hiv_image_80x80x1

---

# TestRandomVariableFunctions

## Functionality Tested:

- Image::AddNoise called via the following methods:

    - Image::AddNoiseFromUniformDistribution
    - Image::AddNoiseFromNormalDistribution
    - Image::AddNoiseFromPoissonDistribution
    - Image::AddNoiseFromGammaDistribution
    - Image::AddNoiseFromExponentialDistribution


## Depends on:

- Image::ReturnDistributionOfRealValues
- EmpiricalDistribution::UpdateDistributionOfRealValues
- EmpiricalDistribution::GetSampleVariance
- EmpiricalDistribution::GetMinimum
- EmpiricalDistribution::GetMaximum
- EmpiricalDistribution::GetSampleSumOfSquares

---
# TestIntegerShifts

## Functionality Tested:

- Image::RotateInPlaceAboutZBy90Degrees(rotate_by_positive_90_degrees)
  - For +90 rotation (in memory)
  - For -90 rotation (in memory)
  - For +90 rotation (in memory, with shift in x + 1 to maintain origin)
  - For -90 rotation (in memory, with shift in y + 1 to maintain origin)
- Image::RealSpaceIntegerShift(-1,0,0);

## Depends on:

- Image::CopyFrom (TestAssignmentOperatorsAndFunctions)

---