import cv2 as cv
import os

SAVE_VIDEOCAP = 0
SAVE_CROP = 1


def save(img, type):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = root_dir
    if type == SAVE_VIDEOCAP:
        if len(img.shape) == 3:
            data_path = os.path.join(root_dir, "ressources/raw-captures/color")
        else:
            data_path = os.path.join(root_dir, "ressources/raw-captures/gray")
    elif type == SAVE_CROP:
        if len(img.shape) == 3:
            data_path = os.path.join(root_dir, "ressources/processed-captures/crops/color")
        else:
            data_path = os.path.join(root_dir, "ressources/processed-captures/crops/gray")
    os.chdir(data_path)
    count = len(os.listdir(data_path))

    cv.imwrite(f'{count}.png', img)
    local_path = data_path.split('\\')[-1]
    print(f'Image saved to: {local_path}/{count}.png')
