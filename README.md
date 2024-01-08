# MESCnn Installation and Modification Guide

For segmenting our glomeruli, we will use the [MESCnn](https://github.com/Nicolik/MESCnn) technology recommended by Dr. Gibier.

## Installation 

Follow the detailed instructions in the [installation document](https://github.com/Nicolik/MESCnn/blob/main/INSTALL.md) on GitHub.

## Modifications

We will make some changes to the code to automate the use of new Whole Slide Images (WSIs) and to obtain 256x256 resolution glomeruli separations without a mask.

### Automating the Use of New WSIs

For segmentation, run the ./run_wsi_tif.py file, which replicates the pipeline for a WSI input. This file automatically downloads WSIs and trained model weights.

In this file, you'll find the following code:
```
download_slides = False
test_tile = True
test_segment = True
test_qu2json = True
test_json2exp = True
test_classify = False
```
Modify these boolean values to perform or skip tasks. The above settings are recommended for improved performance.

To input WSIs, create the path ./Data/Dataset/WSI and place all desired WSIs in this folder.

Modify ./mescnn/detection/qupath/config.py to automate the configuration for all input WSIs. Replace the following code sections (File modified in the segmentation branch):

``` 
Class PathWSI:
    #.....
    #  Code
    #.....
    MESCnn_WSI_BARI = os.path.join(MESCnn_WSI, 'bari_sample_slide.ome.tif')
    MESCnn_WSI_BARI_OPENSLIDE = os.path.join(MESCnn_WSI, 'bari-example-test-slide.tif')
    MESCnn_WSI_COLOGNE = os.path.join(MESCnn_WSI, 'cologne_sample_slide.ome.tif')
    MESCnn_WSI_COLOGNE_2 = os.path.join(MESCnn_WSI, 'cologne_sample_slide_2.ome.tif')
    MESCnn_WSI_SZEGED = os.path.join(MESCnn_WSI, 'szeged_sample_slide.ome.tif')
```
with 
```
Class PathWSI:
    #.....
    #  Code
    #.....

    # List all WSI files
    wsi_files = [f for f in os.listdir(MESCnn_WSI)]
    
    # Create a global variable for each file    
    for f in wsi_files:
        name = f.split('-')[0] if '-' in f else f.split('.')[0]
        globals()['MESCnn_WSI_' + name] = os.path.join(MESCnn_WSI, f)

```
And then replace:

```
def get_test_wsis():
    return [
        PathWSI.MESCnn_WSI_BARI,
        # PathWSI.MESCnn_WSI_BARI_OPENSLIDE,
        PathWSI.MESCnn_WSI_COLOGNE,
        PathWSI.MESCnn_WSI_COLOGNE_2,
        PathWSI.MESCnn_WSI_SZEGED
    ]
```
with
```
def get_test_wsis():
    return [
        #Return all MESCnn_WSI_ files in globals()
        globals()[f] for f in globals() if f.startswith('MESCnn_WSI_')
    ]
```

After these modifications, you can run ./run_wsi_tif.py without further configuration concerns.

### 256x256 Glomeruli Separations Without Mask

The code is originally designed to produce 256x256 resolution glomeruli separations with a black mask. For our project, we need images of the same resolution but without this mask. We modified the ./mescnn/detection/qupath/json2exp.py file accordingly.
(File modified in the segmentation branch)

```
#.....
#  Code
#.....
path_to_crop_256_no_mask = os.path.join(path_to_export_json2exp, "Crop-256-No-Mask")
os.makedirs(path_to_crop_256_no_mask, exist_ok=True)

#.....
#  Code
#.....
subdir_crop_256_no_mask = os.path.join(path_to_crop_256_no_mask, wsi_id)
os.makedirs(subdir_crop_256_no_mask, exist_ok=True)

#.....
#  Code
#.....
cmask256_no_mask_file = os.path.join(subdir_crop_256_no_mask, row['filename'])
orig_resized = cv2.resize(orig, (256, 256), interpolation=cv2.INTER_LINEAR)
cv2.imwrite(cmask256_no_mask_file, orig_resized)
```

## Issues

Any issues encountered during execution are addressed in the [installation file](https://github.com/Nicolik/MESCnn/blob/main/INSTALL.md). However, if you plan to run the code without an Nvidia GPU, you might encounter errors.
