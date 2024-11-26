import os
import warnings
import cv2
from hpacellseg.utils import label_cell


warnings.simplefilter(action="ignore", category=FutureWarning)

# Simple code that runs the model on inference for them and saves the masks images
def create_masks(segmentator, image_stack, output_folder, output_prefix):
    nuc_segmentation = segmentator.pred_nuclei(image_stack[2])
    cell_segmentation = segmentator.pred_cells(image_stack)

    # post-processing nuclei and cell mask
    for i, (nuc_segmentation, cell_segmentation) in enumerate(zip(nuc_segmentation, cell_segmentation)):
        nuclei_mask, cell_mask = label_cell(nuc_segmentation, cell_segmentation)
        cv2.imwrite(os.path.join(output_folder, output_prefix + "nucleimask.png"), nuclei_mask)
        cv2.imwrite(os.path.join(output_folder, output_prefix + "cellmask.png"), cell_mask)
