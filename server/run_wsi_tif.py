import os
import logging
import subprocess
import pandas as pd
import time

from mescnn.definitions import ROOT_DIR
from mescnn.classification.gutils.config import OxfordModelNameCNN
from mescnn.detection.model.config import SegmentationModelName
from mescnn.detection.qupath.config import PathMESCnn, PathWSI, get_test_wsis

def mescnn_function(socketio, room_id, process_data):

    # Find files in the folder "current-file"
    files = os.listdir('./current-files/')
    path = './current-files/' + files[0]

    # Get the WSI and the type of the WSI
    get_wsi_path = get_test_wsis(path)
    wsis = get_wsi_path[0]
    type_wsi = get_wsi_path[1]

    # Tests
    test_tile = True
    test_segment = True
    test_qu2json = True
    test_json2exp = True
    test_classify = True

    #! Initialisation
    start_time = time.time()

    wsi_tiff_dir = PathWSI.MESCnn_WSI
    detection_model = SegmentationModelName.CASCADE_R_50_FPN_3x
    path_to_export = os.path.join(PathWSI.MESCnn_EXPORT, detection_model)
    qupath_segm_dir = os.path.join(path_to_export, 'QuPathProject')

    #! Loading effectué
    socketio.emit('message', {"text": 'Loading complete!', "step": -1}, room=room_id)
    socketio.emit('message', {"text": 'Processing image...', "step": -1}, room=room_id)
    socketio.sleep(1)

    if test_tile:
        print(wsis)
        print(type_wsi)
        if wsis[0] is False:
            logging.info("No WSIs found for testing!")
            return
        elif type_wsi == "wsi":
            for wsi in wsis:
                logging.info(f"{PathMESCnn.TILE} running on {wsi}...")
                subprocess.run(["python", PathMESCnn.TILE,
                                "--wsi", wsi,
                                "--export", path_to_export])
        else:
            test_segment = False
            test_qu2json = False
            test_json2exp = False
                
    #! Tiling effectué
    if type_wsi == "wsi":
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
    if type_wsi == "wsi":
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
    if type_wsi == "wsi":
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
    if type_wsi == "wsi":
        socketio.emit('message', {"text": 'Crops generated!', "step": 2}, room=room_id)
        socketio.sleep(0.2)
    

    if test_classify:
        net_M = OxfordModelNameCNN.EfficientNet_V2_M
        net_E = OxfordModelNameCNN.EfficientNet_V2_M
        net_S = OxfordModelNameCNN.DenseNet161
        net_C = OxfordModelNameCNN.MobileNet_V2
        use_vit = False
        
        if type_wsi == "img":
            img = True
        else:
            img = False

        use_vit_M = use_vit_E = use_vit_S = use_vit_C = use_vit
        if type_wsi == "wsi":
            socketio.emit('message', {"text": 'Calculating Oxford score', "step": -1}, room=room_id)
        else :
            socketio.emit('message', {"text": 'Calculating score for image', "step": -1}, room=room_id)
        logging.info(f"Running {PathMESCnn.CLASSIFY} with {net_M}, {net_E}, {net_S}, {net_C}")
        subprocess.run(["python", PathMESCnn.CLASSIFY,
                        "--root-path", ROOT_DIR,
                        "--export-dir", path_to_export,
                        "--netM", net_M, "--vitM", str(use_vit_M),
                        "--netE", net_E, "--vitE", str(use_vit_E),
                        "--netS", net_S, "--vitS", str(use_vit_S),
                        "--netC", net_C, "--vitC", str(use_vit_C),
                        "--path_wsi", wsis[0],
                        "--img", str(img)]),

    else:
        logging.info(f"Skipping run of {PathMESCnn.CLASSIFY}")

    end_time = time.time()
    processing_time = end_time - start_time

    process_data.file_name = files[0]
    process_data.time = processing_time
    process_data.type = type_wsi

    update_server_data(process_data)

    #! Fin
    socketio.emit('message', {"text": 'Score determined!', "step": 3}, room=room_id)
    socketio.sleep(2)
    socketio.emit('message', {"text": '', "step": 4}, room=room_id)


def update_server_data(process_data):
    
    base_path = "./Data/Export/cascade_R_50_FPN_3x/"

    report_dir = "Report/M-efficientnetv2-m_E-efficientnetv2-m_S-densenet161_C-mobilenetv2/"
    wsi_path = os.listdir(base_path + report_dir)
    
    # Remove the file with Oxford in it
    wsi_path = [w for w in wsi_path if 'Oxford' not in w]
    wsi_path = wsi_path[0]

    #! Classification
    
    # Create a dataframe, first row is the header
    csv_content = pd.read_csv(base_path + report_dir + "/" + wsi_path, sep=';', header=None)
    df = csv_content.values.tolist()
    df = pd.DataFrame(df[1:], columns=df[0])

    process_data.classification_csv = df.copy()

    # Calculate the histogram using the columns of the dataframe
    histogram = df.iloc[:, 5:9].astype('float').sum().to_dict()

    # Only keep the first character of the column name (M-bin -> M)
    histogram = {k[0]: v for k, v in histogram.items()}
    histogram['total'] = len(df)

    process_data.crop_amount = len(df)

    #! Oxford score

    if process_data.type == "wsi":
        
        df = pd.read_csv(base_path + '/Report/M-efficientnetv2-m_E-efficientnetv2-m_S-densenet161_C-mobilenetv2/Oxford.csv', sep=';')
        # Only keep the values if the WSI-ID is contained in the filename
        df = df[df['WSI-ID'].str.contains(process_data.file_name.split('.')[0])]

        # Only keep columns with "-score" in it
        df = df[[c for c in df.columns if '-score' in c]]

        # Only keep the second character of each value
        df = df.map(lambda x: int(x[1]))

        # Only keep the first character of the column name
        df.columns = [c[0] for c in df.columns]

        # Transform to dictionary
        oxford = df.to_dict(orient='records')[0]

        process_data.histogram = histogram
        process_data.score = oxford
        