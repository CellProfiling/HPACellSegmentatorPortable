import os
import warnings
import cv2
import hpacellseg.cellsegmentator as cellsegmentator
from hpacellseg.utils import label_cell, label_nuclei


warnings.simplefilter(action="ignore", category=FutureWarning)

# Path definitions

# Models refered are downloaded from (can't add them to github due to size limits):
#    "https://zenodo.org/record/4665863/files/dpn_unet_nuclei_v1.pth"
#    "https://zenodo.org/record/4665863/files/dpn_unet_cell_3ch_v1.pth"
NUC_MODEL = "./models/dpn_unet_nuclei_v1.pth"
CELL_MODEL = "./models/dpn_unet_cell_3ch_v1.pth"
# Input folder expects to have blue - nuclei, red - microtubules, yellow - ER images in PNG format with specific suffixes
#    green - protein iamge is not needed for cell segmentation, just there for completition sake
image_path = "./input"
mask_path = "./output"


# Simple code that reads images, runs the model on inference for them and saves the masks images
def create_masks(segmentator, image_path, mask_path):
    image_name = ""
    image_mt = None
    image_er = None
    image_nuc = None
    for input_file in os.listdir(image_path):
        if input_file.endswith("_blue.png"):
            image_nuc = cv2.imread(image_path + "/" + input_file, -1)
            image_name = input_file.replace("_blue.png", "")
        elif input_file.endswith("_red.png"):
            image_mt = cv2.imread(image_path + "/" + input_file, -1)
        elif input_file.endswith("_yellow.png"):
            image_er = cv2.imread(image_path + "/" + input_file, -1)

    if image_mt is None or image_er is None or image_nuc is None:
        print(f"Image not found")
        return

    image = [[image_mt], [image_er], [image_nuc]]

    nuc_segmentation = segmentator.pred_nuclei(image[2])
    cell_segmentation = segmentator.pred_cells(image)

    nuclei_mask, cell_mask = label_cell(nuc_segmentation[0], cell_segmentation[0])

    cv2.imwrite(mask_path + "/" + image_name + "_nucleimask.png", nuclei_mask)
    cv2.imwrite(mask_path + "/" + image_name + "_cellmask.png", cell_mask)


# Main code simplified
segmentator = cellsegmentator.CellSegmentator(NUC_MODEL, CELL_MODEL, device="cuda", padding=True, multi_channel_model=True)
create_masks(segmentator, image_path, mask_path)
