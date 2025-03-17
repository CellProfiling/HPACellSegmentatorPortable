import warnings
import numpy as np
from skimage.measure import regionprops
from scipy.ndimage.morphology import grey_dilation
import pandas as pd
import cv2


warnings.simplefilter(action="ignore", category=FutureWarning)
colors = ["red", "yellow", "blue", "green"]


def safe_crop(image, bbox):
    x1, y1, x2, y2 = bbox
    img_w, img_h = image.shape[:2]
    is_single_channel = len(image.shape) == 2
    if x1 < 0:
        pad_x1 = 0 - x1
        new_x1 = 0
    else:
        pad_x1 = 0
        new_x1 = x1
    if y1 < 0:
        pad_y1 = 0 - y1
        new_y1 = 0
    else:
        pad_y1 = 0
        new_y1 = y1
    if x2 > img_w - 1:
        pad_x2 = x2 - (img_w - 1)
        new_x2 = img_w - 1
    else:
        pad_x2 = 0
        new_x2 = x2
    if y2 > img_h - 1:
        pad_y2 = y2 - (img_h - 1)
        new_y2 = img_h - 1
    else:
        pad_y2 = 0
        new_y2 = y2

    patch = image[new_x1:new_x2, new_y1:new_y2]
    patch = (
        np.pad(
            patch,
            ((pad_x1, pad_x2), (pad_y1, pad_y2)),
            mode="constant",
            constant_values=0,
        )
        if is_single_channel
        else np.pad(
            patch,
            ((pad_x1, pad_x2), (pad_y1, pad_y2), (0, 0)),
            mode="constant",
            constant_values=0,
        )
    )
    return patch, (new_x1, new_y1, new_x2, new_y2)


# Optional code to generate the segmented cell crops
def generate_crops(image_stack, cell_mask, crop_size, mask_cell, output_folder, output_prefix):
    regions = regionprops(cell_mask)

    cell_bboxes = []
    for region in regions:
        image_cp = image_stack[0][0].copy()

        bbox = region.bbox
        bbox_center = [(bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2]
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        fixed_bbox = (
            bbox_center[0] - crop_size // 2,
            bbox_center[1] - crop_size // 2,
            bbox_center[0] + crop_size // 2,
            bbox_center[1] + crop_size // 2,
        )

        for curr_img_index in range(len(image_stack)):
            if curr_img_index != 0:
                image_cp = image_stack[curr_img_index][0].copy()

            cell_crop, _ = safe_crop(image_cp, fixed_bbox)
            cv2.imwrite(f"{output_folder}/{output_prefix}cell{region.label}_crop_" + colors[curr_img_index] + ".png", cell_crop)

            if mask_cell:
                this_cell_mask = cell_mask == region.label
                this_cell_mask = grey_dilation(this_cell_mask, size=7)
                image_cp[this_cell_mask == 0] = 0
                cell_mask_crop, _ = safe_crop(image_cp, fixed_bbox)
                cv2.imwrite(f"{output_folder}/{output_prefix}cell{region.label}_crop_masked_" + colors[curr_img_index] + ".png", cell_mask_crop)

        new_center = (crop_size // 2, crop_size // 2)
        new_bbox = (
            new_center[0] - w // 2,
            new_center[1] - h // 2,
            new_center[0] + w // 2,
            new_center[1] + h // 2,
        )
        cell_bboxes.append(
            {
                "id" : output_prefix,
                "cell": region.label,
                "x1": new_bbox[0],
                "y1": new_bbox[1],
                "x2": new_bbox[2],
                "y2": new_bbox[3],
            }
        )

    return pd.DataFrame(cell_bboxes)





