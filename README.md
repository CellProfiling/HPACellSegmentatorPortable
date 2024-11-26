HPA Cell Segmentator Portable
=============================

Just a repackage of the "HPA Cell Segmentator" repository with updated libraries and simplified usage. 


Installation
------------

If you use any Python IDE (VSCode, PyCharm, Spyder, etc...), just:
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

`r_image,y_image,b_image,g_image,output_folder,output_prefix`

- `r_image`: the microtubules targeting marker FOV image. 
- `y_image`: the ER targeting marker FOV image.
- `b_image`: the nuclei targeting marker FOV image.
- `output_folder`: the base folder that will contain all results.
- `output_prefix`: the prefix appended to all files generated per cell.

All images can be relative or absolute paths, or directly URLs. You can also skip cells between runs with the special character `#` in front of the desired lines. 
Check the following `path_list.csv` content as an example:

```
#r_image,y_image,b_image,output_folder,output_prefix
images/CACO-2_2047_C3_6_red.png,images/CACO-2_2047_C3_6_yellow.png,images/CACO-2_2047_C3_6_blue.png,output,CACO-2_2047_C3_6_
#images/CACO-2_2047_C3_7_red.png,images/CACO-2_2047_C3_7_yellow.png,images/CACO-2_2047_C3_7_blue.png,output,CACO-2_2047_C3_7_
images/U-215MG792_H7_2_red.png,images/U-215MG792_H7_2_yellow.png,images/U-215MG792_H7_2_blue.png,output,U-215MG792_H7_2_
```

Once you have prepared your `path_list.csv` and put it in your virtual environment you are ready to run the `process.py` script. Simply call `python process.py` or run it directly in your IDE.


Output
------ 

HPACellSegmentatorPortable model creates the following items per each cell crop input:
- `[output_prefix]_cellmask.png`: the labeled image containing the segmented cells.
- `[output_prefix]_nucleimask.png`: the labeled image containing the segmented nucleis.
