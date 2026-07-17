HPA Cell Segmentator Portable
=============================

Just a repackage of the "HPA Cell Segmentator" repository with updated libraries and simplified usage. 


Installation
------------

**As a package (recommended).** From the repository root:

- `pip install .` to install it, or `pip install -e .` for an editable/development install.

This installs three importable top-level packages (`hpacellsegmentator`, `hpacellseg`, `pytorch_zoo`) and three commands:

- `hpacellsegmentator`: segment a single set of images (see *Running the code*).
- `hpacellsegmentator-batch`: process many image sets via `path_list.csv`.
- `hpacellsegmentator-service`: run the HTTP segmentation service.

**Manual/IDE setup.** If you use any Python IDE (VSCode, PyCharm, Spyder, etc...), just:
- Either import the project into your IDE through git/github OR Create a new project and download all the repository code from github into it.
- Create a virtual environment for that project.
- Install the project requirements through your IDE. Make sure the packages versions match, as IDEs try to be too smart some times.

If you want to install it via basic Python virtual environment:
- Install `python3`, `pip` and `virtualenv` in case you don't have them yet.
- Navigate to your desired working directory.
  - Example: `cd /home/lab/sandbox`
- Create a virtual environment:
  - Example: `python3 -m venv HPACellSegmentatorPortable`
- Download/clone all the repository code inside your virtual environment directory.
- Navigate to your virtual environment directory and activate it:
  - Example: `source bin/activate` (linux) or `Scripts\activate.bat` (windows)
- Install all requirements through pip:
  - Example: `pip install -r requirements.txt`
- Profit!


Setup
-----

You need to download the HPACellSegmentator model files. The easiest way to do this is:
- Create a folder in your virtual environment named `models`
- Download the models from here:
  - https://zenodo.org/record/4665863/files/dpn_unet_nuclei_v1.pth
  - https://zenodo.org/record/4665863/files/dpn_unet_cell_3ch_v1.pth
- Put the files into the `models` folder.


Running the code
---------------- 

**NOTE**: remember that you have to access your created virtual environment before running the code! If you are using an IDE you are probably ready to go, but if you have installed a basic python virtual environment remember to activate it like this: 
- Example:
   - `cd /home/lab/sandbox/HPACellSegmentatorPortable`
   - `source bin/activate` (linux) or `Scripts\activate.bat` (windows)

To run HPACellSegmentatorPortable you have first to gather the information about the sets of images you want to process. HPACellSegmentatorPortable reads `path_list.csv` to locate each set of images, in the following .csv format: 

`r_image,y_image,b_image,g_image,segmentation_folder,crop_folder,output_prefix`

- `r_image`: the microtubules targeting marker FOV image. 
- `y_image`: the ER targeting marker FOV image.
- `b_image`: the nuclei targeting marker FOV image.
- `g_image`: the protein targeting marker FOV image (only needed if you want to generate the cell crops).
- `segmentation_folder`: the base folder that will contain all generated segmentations.
- `crop_folder`: the base folder that will contain all generated crops (only needed if you want to generate the cell crops).
- `output_prefix`: the prefix appended to all files generated per cell.

All images can be relative or absolute paths, or directly URLs. You can also skip cells between runs with the special character `#` in front of the desired lines. 
Check the following `path_list.csv` content as an example:

```
#r_image,y_image,b_image,g_image,segmentation_folder,crop_folder,output_prefix
images/CACO-2_2047_C3_6_red.png,images/CACO-2_2047_C3_6_yellow.png,images/CACO-2_2047_C3_6_blue.png,,output,,CACO-2_2047_C3_6_
#images/CACO-2_2047_C3_7_red.png,images/CACO-2_2047_C3_7_yellow.png,images/CACO-2_2047_C3_7_blue.png,,output,,CACO-2_2047_C3_7_
images/U-215MG792_H7_2_red.png,images/U-215MG792_H7_2_yellow.png,images/U-215MG792_H7_2_blue.png,,output,,U-215MG792_H7_2_
```

Once you have prepared your `path_list.csv` you are ready to run the batch script (`hpacellsegmentator/batch.py`, formerly `process.py`). It reads `path_list.csv` and `config.yaml` from the current working directory, so run it from the directory that holds them. You can choose between 3 different running approaches, depending on your personal preferences:

- Edit directly the constants located in the `hpacellsegmentator/batch.py` script:
  - Probably the least versatile, but useful if you are always running HPACellSegmentatorPortable with the same settings.
  - Just change the values under for the following section of code: `# If you want to use constants with your script, add them here` .
  - Simply call `hpacellsegmentator-batch`.

- Call the batch script with arguments:
  - You can get a list of available parameters (and their default values) using `-help` or `-?` argument.
  - Example call: `hpacellsegmentator-batch -c True -cs 684`.
- Call `process.py` script with arguments:
  - You can get a list of available parameters using the `-h` or `--help` argument.
  - Boolean options are toggled with a flag: use `-c`/`--crop_cells` to enable or `--no-crop_cells` to disable (likewise `-cm`/`--crop_mask` and `-mc`/`--mask_cell`).
  - Value options take a number: `-cs`/`--crop_size` and `-cb`/`--crop_bitdepth`.
  - Example call: `python process.py --crop_cells --crop_size 684`.

- Edit the `config.yaml` file:
  - Just change the contents of the file with your desired values.
  - Simply call `hpacellsegmentator-batch`.

If you have not installed the package, `python -m hpacellsegmentator.batch` works the same way from the repository root.

These approaches can be combined; when a parameter is set in more than one place, command line arguments take precedence over `config.yaml`, which in turn takes precedence over the constants in `process.py`.

**NOTE**: `config.yaml` must always be present (it can be left empty). If the file is missing, `process.py` will fail to start.


Output
------ 

HPACellSegmentatorPortable model creates the following items in the chosen segmentation folder per each FOV input:
- `[output_prefix]_cellmask.png`: the labeled image containing the segmented cells.
- `[output_prefix]_nucleimask.png`: the labeled image containing the segmented nucleis.

If the generating crops option has been selected, HPACellSegmentatorPortable will also generate in the chosen crop_folder the following files:
- `[output_prefix]_cell[X]_crop_[red|yellow|blue|green].png`: a cropped cell from the FOV.
- `[output_prefix]_cell[X]_crop_masked_[red|yellow|blue|green].png`: a cropped and masked cell from the FOV (if the mask_cell option was selected).
- `[output_prefix]_cell[X]_mask.png`: the binary cell mask for that crop (if the crop_mask option was selected).
- `[output_prefix]_cell[X]_nucleimask.png`: the binary nuclei mask for that crop (if the crop_mask option was selected).
- Additionally, a `crop_info.csv` file will be created containing all generated cell crops bboxes for convenience.