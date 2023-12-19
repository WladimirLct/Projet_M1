import os
from enum import IntEnum

from mescnn.definitions import ROOT_DIR

MAGNIFICATION = 40
MIN_AREA_GLOMERULUS_UM = 5000
MIN_AREA_BBOX_GLOMERULUS = 5000
DETECTRON_SCORE_THRESHOLD = 0.5


class PathMESCnn:
    SEGMENT_PROJECT = os.path.join(ROOT_DIR, "mescnn", "detection", "qupath", "segment_project.py")
    TILE = os.path.join(ROOT_DIR, "mescnn", "detection", "qupath", "tile.py")
    SEGMENT = os.path.join(ROOT_DIR, "mescnn", "detection", "qupath", "segment.py")
    PKL2QU = os.path.join(ROOT_DIR, "mescnn", "detection", "qupath", "pkl2qu.py")
    QU2JSON = os.path.join(ROOT_DIR, "mescnn", "detection", "qupath", "qu2json.py")
    JSON2EXP = os.path.join(ROOT_DIR, "mescnn", "detection", "qupath", "json2exp.py")
    INFERENCE = os.path.join(ROOT_DIR, "mescnn", "detection", "model", "inference.py")
    CLASSIFY = os.path.join(ROOT_DIR, "mescnn", "classification", "inference", "classify.py")
    COLLATE_CLASSIFY = os.path.join(ROOT_DIR, "classification", "inference", "collate_classify.py")


class PathWSI:
    BASE_MESCnn = os.path.join(ROOT_DIR, 'Data')
    MESCnn_EXPORT = os.path.join(BASE_MESCnn, 'Export')

    MESCnn_DATASET = os.path.join(BASE_MESCnn, 'Dataset')
    QUPATH_MESCnn_DIR_NOANN = os.path.join(MESCnn_DATASET, 'QuPathProject-NoAnnotations')

    MESCnn_WSI = os.path.join(MESCnn_DATASET, 'WSI')

    # List all WSI files
    wsi_files = [f for f in os.listdir(MESCnn_WSI)]
    
    # Create a global variable for each file    
    for f in wsi_files:
        name = f.split('-')[0] if '-' in f else f.split('.')[0]
        globals()['MESCnn_WSI_' + name] = os.path.join(MESCnn_WSI, f)



def get_test_wsis():
    return [
        #Return all MESCnn_WSI_ files in globals()
        globals()[f] for f in globals() if f.startswith('MESCnn_WSI_')
    ]


class GlomerulusDetection(IntEnum):
    BACKGROUND = 0
    GLOMERULUS = 1


def init_data_dict():
    return {
        'image-id': [],
        'filename': [],
        'path-to-wsi': [],
        'ext': [],
        's': [],
        'x': [],
        'y': [],
        'w': [],
        'h': []
    }
