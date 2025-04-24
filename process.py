import argparse
import datetime
import logging
import os
import sys
import yaml
import pandas as pd

import cv2
import generate_masks
import generate_cell_crops
import hpacellseg.cellsegmentator as cellsegmentator
from skimage.io import imread


# This is the log configuration. It will log everything to a file AND the console
logging.basicConfig(
    filename="log.txt",
    encoding="utf-8",
    format="%(levelname)s: %(message)s",
    filemode="w",
    level=logging.INFO,
)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logger = logging.getLogger("HPACellSegmentatorPortable")

# This is the general configuration variable. We are going to use the special key "log" in the dictionary to use the log in our code
config = {"log": logger}

# If you want to use constants with your script, add them here
config["crop_cells"] = True
config["crop_size"] = 1024
config["crop_bitdepth"] = 8
config["crop_mask"] = True
config["mask_cell"] = True

# If you want to use command line parameters with your script, add them here
if len(sys.argv) > 1:
    argparser = argparse.ArgumentParser(
        description="Please input the following parameters"
    )
    argparser.add_argument(
        "-c",
        "--crop_cells",
        help="if you want to generate the crops of the cells detected in the segmentation",
        default=False,
        type=bool,
    )
    argparser.add_argument(
        "-cs",
        "--crop_size",
        help="the cell crop size",
        default=1024,
        type=int,
    )
    argparser.add_argument(
        "-cb",
        "--crop_bitdepth",
        help="the cell crop bitdepth",
        default=8,
        type=int,
    )
    argparser.add_argument(
        "-cm",
        "--crop_mask",
        help="if you want to also generate the crop binary mask from the segmentation",
        default=False,
        type=bool,
    )
    argparser.add_argument(
        "-mc",
        "--mask_cell",
        help="if you want additional crops with only the segmented cell area",
        default=False,
        type=bool,
    )

    args = argparser.parse_args()
    config = config | args.__dict__

# If you want to use a configuration file with your script, add it here
with open("config.yaml", "r") as file:
    config_contents = yaml.safe_load(file)
    if config_contents:
        config = config | config_contents

# Log the start time and the final configuration so you can keep track of what you did
config["log"].info("Start: " + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
config["log"].info("Parameters used:")
config["log"].info(config)
config["log"].info("----------")

try:
    # We load the CellSegmentator model
    segmentator = cellsegmentator.CellSegmentator(
        "./models/dpn_unet_nuclei_v1.pth",
        "./models/dpn_unet_cell_3ch_v1.pth",
        device="cuda", padding=True, multi_channel_model=True)

    # if we want to generate the crops, we are going to keep their information in a CSV file
    if config["crop_cells"]:
        df = pd.DataFrame(columns=['id', 'cell', 'x1', 'y1', 'x2', 'y2'])

    # We iterate over each set of images to process
    if os.path.exists("./path_list.csv"):
        path_list = open("./path_list.csv", "r")
        for curr_set in path_list:

            if curr_set.strip() != "" and not curr_set.startswith("#"):
                curr_set_arr = curr_set.split(",")
                # We create the output folder
                os.makedirs(curr_set_arr[4].strip(), exist_ok=True)
                # We load the images as numpy arrays
                image_stack = []
                image_stack.append([cv2.imread(curr_set_arr[0].strip(), cv2.IMREAD_GRAYSCALE)])
                image_stack.append([cv2.imread(curr_set_arr[1].strip(), cv2.IMREAD_GRAYSCALE)])
                image_stack.append([cv2.imread(curr_set_arr[2].strip(), cv2.IMREAD_GRAYSCALE)])

                # We run the model
                cell_mask = generate_masks.create_masks(segmentator, image_stack, curr_set_arr[4].strip(), curr_set_arr[6].strip())
                # Single cell crops
                if config["crop_cells"]:
                    os.makedirs(curr_set_arr[5].strip(), exist_ok=True)
                    image_stack.append([cv2.imread(curr_set_arr[3].strip(), cv2.IMREAD_GRAYSCALE)])
                    cell_bbox_df = generate_cell_crops.generate_crops(image_stack, cell_mask, config["crop_size"], config["crop_bitdepth"], config["crop_mask"], config["mask_cell"], curr_set_arr[5].strip(), curr_set_arr[6].strip())
                    df = pd.concat([df, cell_bbox_df], ignore_index=True)

                config["log"].info("- Saved results for " + curr_set_arr[6].strip())

        # We store the cell crops bboxes and ids for easy localization
        if config["crop_cells"]:
            df.to_csv("crop_info.csv", index=False)
except Exception as e:
    config["log"].error("- " + str(e))

config["log"].info("----------")
config["log"].info("End: " + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
