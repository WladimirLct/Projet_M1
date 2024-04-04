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
    
    #/home/antoine/Documents/GitHub/MESCnn/Data/Dataset/WSI/C2321120-1-A-PAS(1).svs
    BASE_MESCnn = os.path.join(ROOT_DIR, 'Data')
    MESCnn_EXPORT = os.path.join(BASE_MESCnn, 'Export')

    MESCnn_DATASET = os.path.join(BASE_MESCnn, 'Dataset')
    QUPATH_MESCnn_DIR_NOANN = os.path.join(MESCnn_DATASET, 'QuPathProject-NoAnnotations')

    MESCnn_WSI = os.path.join(ROOT_DIR, 'current-file')
    
    # MESCnn_WSI_BARI = os.path.join(MESCnn_WSI, 'bari_sample_slide.ome.tif')
    # MESCnn_WSI_BARI_OPENSLIDE = os.path.join(MESCnn_WSI, 'bari-example-test-slide.tif')
    # MESCnn_WSI_COLOGNE = os.path.join(MESCnn_WSI, 'cologne_sample_slide.ome.tif')
    # MESCnn_WSI_COLOGNE_2 = os.path.join(MESCnn_WSI, 'cologne_sample_slide_2.ome.tif')
    # MESCnn_WSI_SZEGED = os.path.join(MESCnn_WSI, 'szeged_sample_slide.ome.tif')

def get_test_wsis(path):
    # Liste des extensions de fichier valides
    valid_extensions = ('.ndpi', '.svs', '.mrxs', '.tif', '.tiff', '.scn', '.ome.tiff', '.ome.tif')

    if path:
        # Vérification que le chemin pointe vers un fichier existant
        if os.path.isfile(path):
            # Extraction de l'extension du fichier à partir du chemin
            _, ext = os.path.splitext(path)

            # Vérification que l'extension du fichier est valide
            if ext in valid_extensions:
                return [path]
            else:
                print("L'extension du fichier n'est pas valide.")
                return [False]
        else:
            print("Le fichier n'existe pas.")
            return [False]
    else:
        return [False] 


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
