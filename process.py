import datetime
import logging
import os

import generate_masks
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

    # We iterate over each set of images to process
    if os.path.exists("./path_list.csv"):
        path_list = open("./path_list.csv", "r")
        for curr_set in path_list:

            if curr_set.strip() != "" and not curr_set.startswith("#"):
                curr_set_arr = curr_set.split(",")
                # We create the output folder
                os.makedirs(curr_set_arr[3].strip(), exist_ok=True)
                # We load the images as numpy arrays
                image_stack = []
                image_stack.append([imread(curr_set_arr[0].strip(), as_gray=True)])
                image_stack.append([imread(curr_set_arr[1].strip(), as_gray=True)])
                image_stack.append([imread(curr_set_arr[2].strip(), as_gray=True)])

                # We run the model
                generate_masks.create_masks(segmentator, image_stack, curr_set_arr[3].strip(), curr_set_arr[4].strip())

                config["log"].info("- Saved results for " + curr_set_arr[4].strip())
except Exception as e:
    config["log"].error("- " + str(e))

config["log"].info("----------")
config["log"].info("End: " + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
