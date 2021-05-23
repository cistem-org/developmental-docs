# CPU data io


## Sample location and files

The code relevant for this How-To can be found in: [cisTEM/src/programs/samples/0_Simple/disk_io_image.cpp](https://github.com/bHimes/cisTEM_downstream_bah/blob/development/src/programs/samples/0_Simple/disk_io_image.cpp)

### Quick and dirty

Images may be read from, and written to disk using a set of "quick and dirty" methods in the ***IMAGE*** class.

```java
int slice_to_read = 1; // read the first slice in Z
Image my_image;
my_image.QuickAndDirtyReadSlice("/path/to/my/image", slice_to_read)
```
--> see: [QuickAndDirtyReadSlice](../../reference/classes/Image/QuickAndDirtyReadSlice.md) 
 %        [QuickAndDirtyReadSlices]() 
 %       [QuickAndDirtyWriteSlice]() 
 %        [QuickAndDirtyWriteSlices]()



