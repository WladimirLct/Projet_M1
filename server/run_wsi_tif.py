import os
import logging
import subprocess

from mescnn.definitions import ROOT_DIR
from mescnn.classification.gutils.config import OxfordModelNameCNN
from mescnn.detection.model.config import SegmentationModelName
from mescnn.detection.qupath.config import PathMESCnn, PathWSI, get_test_wsis

def mescnn_function(socketio, room_id):

    # Find files in the folder "current-file"
    files = os.listdir('./current-file/')
    path = './current-file/' + files[0]

    wsis = get_test_wsis(path)

    # Tests
    test_tile = True
    test_segment = True
    test_qu2json = True
    test_json2exp = True
    test_classify = True

    wsi_tiff_dir = PathWSI.MESCnn_WSI
    detection_model = SegmentationModelName.CASCADE_R_50_FPN_3x
    path_to_export = os.path.join(PathWSI.MESCnn_EXPORT, detection_model)
    qupath_segm_dir = os.path.join(path_to_export, 'QuPathProject')

    #! Loading effectué
    socketio.emit('message', {"text": 'Loading complete!', "step": -1}, room=room_id)
    socketio.emit('message', {"text": 'Processing image...', "step": -1}, room=room_id)
    socketio.sleep(1)

    if test_tile:
        if wsis[0] is False:
            logging.info("No WSIs found for testing!")
            return
        else:
            for wsi in wsis:
                logging.info(f"{PathMESCnn.TILE} running on {wsi}...")
                subprocess.run(["python", PathMESCnn.TILE,
                                "--wsi", wsi,
                                "--export", path_to_export])
                
    #! Tiling effectué
    socketio.emit('message', {"text": 'Tiling complete!', "step": 0}, room=room_id)
    socketio.sleep(0.2)

    if test_segment:
        for wsi in wsis:
            socketio.emit('message', {"text": 'Segmentation masks in progess...', "step": -1}, room=room_id)
            logging.info(f"{PathMESCnn.SEGMENT} running on {wsi}...")
            subprocess.run(["python", PathMESCnn.SEGMENT,
                            "--wsi", wsi,
                            "--export", path_to_export,
                            "--qupath", qupath_segm_dir,
                            "--model", detection_model])
    else:
        logging.info(f"Skipping run of {PathMESCnn.SEGMENT}!")

    #! Masques de segmentation effectués
    socketio.emit('message', {"text": 'Masks generated!', "step": 1}, room=room_id)
    socketio.sleep(0.2)

    if test_qu2json:
        socketio.emit('message', {"text": 'Annotation conversion in progress...', "step": -1}, room=room_id)
        logging.info(f"Running {PathMESCnn.QU2JSON}")
        subprocess.run(["python", PathMESCnn.QU2JSON,
                        "--export", path_to_export,
                        "--wsi-dir", wsi_tiff_dir,
                        "--qupath", qupath_segm_dir])
    else:
        logging.info(f"Skipping run of {PathMESCnn.QU2JSON}")

    #! Conversion QuPath -> JSON effectuée
    socketio.emit('message', {"text": 'Masks converted to JSON!', "step": -1}, room=room_id)
    socketio.sleep(0.2)

    if test_json2exp:
        socketio.emit('message', {"text": 'Annotation export in progress...', "step": -1}, room=room_id)
        logging.info(f"Running {PathMESCnn.JSON2EXP}")
        subprocess.run(["python", PathMESCnn.JSON2EXP,
                        "--export", path_to_export,
                        "--wsi-dir", wsi_tiff_dir])
    else:
        logging.info(f"Skipping run of {PathMESCnn.JSON2EXP}")

    #! Exportation des glomérules effectuée
    socketio.emit('message', {"text": 'Crops generated!', "step": 2}, room=room_id)
    socketio.sleep(0.2)

    if test_classify:
        net_M = OxfordModelNameCNN.EfficientNet_V2_M
        net_E = OxfordModelNameCNN.EfficientNet_V2_M
        net_S = OxfordModelNameCNN.DenseNet161
        net_C = OxfordModelNameCNN.MobileNet_V2
        use_vit = False

        use_vit_M = use_vit_E = use_vit_S = use_vit_C = use_vit
        socketio.emit('message', {"text": 'Calculating Oxford score', "step": -1}, room=room_id)
        logging.info(f"Running {PathMESCnn.CLASSIFY} with {net_M}, {net_E}, {net_S}, {net_C}")
        subprocess.run(["python", PathMESCnn.CLASSIFY,
                        "--root-path", ROOT_DIR,
                        "--export-dir", path_to_export,
                        "--netM", net_M, "--vitM", str(use_vit_M),
                        "--netE", net_E, "--vitE", str(use_vit_E),
                        "--netS", net_S, "--vitS", str(use_vit_S),
                        "--netC", net_C, "--vitC", str(use_vit_C)])
    else:
        logging.info(f"Skipping run of {PathMESCnn.CLASSIFY}")

    #! Fin
    socketio.emit('message', {"text": 'Score determined!', "step": 3}, room=room_id)
    socketio.sleep(2)
    socketio.emit('message', {"text": '', "step": 4}, room=room_id)