# MESCnn Installation And Modification

Pour la segmentation de nos glomérules, nous allons utiliser la technologie que le Docteur Gibier nous a conseillée : [MESCnn](https://github.com/Nicolik/MESCnn)

## Installation 

Pour l'installation vous pouvez suivre l'excellent [document](https://github.com/Nicolik/MESCnn/blob/main/INSTALL.md) prévu à cet effet sur GitHub.

## Modification 

Nous allons apporter quelques modifications au code afin d'automatiser l'utilisation de nouvelles WSI, mais aussi d'avoir des séparations de glomérules de résolution 256x256 sans masque.

### Automatiser l'utilisation de nouvelles wsi

Pour la segmentation, nous allons exécuter le fichier `./run_wsi_tif.py` qui réplique le pipeline à partir de l'entrée d'un WSI.
Il faut savoir que ce fichier effectue un téléchargement de WSI et des poids des modèles entraînés automatiquement.

Dans ce fichier, on peut retrouver le code suivant :
```
download_slides = False
test_tile = True
test_segment = True
test_qu2json = True
test_json2exp = True
test_classify = False
```
Vous pouvez donc modifier la valeur binaire pour effectuer ou non la tâche. Afin d'améliorer les performances, je vous conseille d'utiliser le paramétrage ci-dessus.

Pour mettre des WSI en input, il faut créer le chemin suivant `./Data/Dataset/WSI`. On peut maintenant déposer dans ce dossier toutes les WSI souhaitées.

Afin d'exécuter `./run_wsi_tif.py` sans problème, nous allons modifier le fichier `./mescnn/detection/qupath/config.py` pour automatiser la configuration de tous les WSI en input.
On remplace donc les parties de code suivantes :

``` 
Class PathWSI:
    #.....
    #  Code
    #.....
    MESCnn_WSI_BARI = os.path.join(MESCnn_WSI, 'bari_sample_slide.ome.tif')
    MESCnn_WSI_BARI_OPENSLIDE = os.path.join(MESCnn_WSI, 'bari-example-test-slide.tif')
    MESCnn_WSI_COLOGNE = os.path.join(MESCnn_WSI, 'cologne_sample_slide.ome.tif')
    MESCnn_WSI_COLOGNE_2 = os.path.join(MESCnn_WSI, 'cologne_sample_slide_2.ome.tif')
    MESCnn_WSI_SZEGED = os.path.join(MESCnn_WSI, 'szeged_sample_slide.ome.tif')
```
par 
```
Class PathWSI:
    #.....
    #  Code
    #.....

    # List all WSI files
    wsi_files = [f for f in os.listdir(MESCnn_WSI)]
    
    # Create a global variable for each file    
    for f in wsi_files:
        name = f.split('-')[0] if '-' in f else f.split('.')[0]
        globals()['MESCnn_WSI_' + name] = os.path.join(MESCnn_WSI, f)

```
Et ensuite :

```
def get_test_wsis():
    return [
        PathWSI.MESCnn_WSI_BARI,
        # PathWSI.MESCnn_WSI_BARI_OPENSLIDE,
        PathWSI.MESCnn_WSI_COLOGNE,
        PathWSI.MESCnn_WSI_COLOGNE_2,
        PathWSI.MESCnn_WSI_SZEGED
    ]
```
par 
```
def get_test_wsis():
    return [
        #Return all MESCnn_WSI_ files in globals()
        globals()[f] for f in globals() if f.startswith('MESCnn_WSI_')
    ]
```

Après ces modifications dans le fichier, vous pouvez lancer `./run_wsi_tif.py` sans plus jamais vous inquiéter des configurations.

### Séparations de glomérules de résolution 256x256 sans masque

Le code est normalement fait pour avoir des séparations de glomérules en résolution 256x256 avec un masque noir. Pour notre projet, nous avons besoin d'images de même résolution mais sans ce masque. Nous avons donc modifié le code du fichier`./mescnn/detection/qupath/json2exp.py`.

```
#.....
#  Code
#.....
path_to_crop_256_no_mask = os.path.join(path_to_export_json2exp, "Crop-256-No-Mask")
os.makedirs(path_to_crop_256_no_mask, exist_ok=True)

#.....
#  Code
#.....
subdir_crop_256_no_mask = os.path.join(path_to_crop_256_no_mask, wsi_id)
os.makedirs(subdir_crop_256_no_mask, exist_ok=True)

#.....
#  Code
#.....
cmask256_no_mask_file = os.path.join(subdir_crop_256_no_mask, row['filename'])
orig_resized = cv2.resize(orig, (256, 256), interpolation=cv2.INTER_LINEAR)
cv2.imwrite(cmask256_no_mask_file, orig_resized)
```

## Problèmes

Tous les problèmes que vous pourriez avoir en exécutant sont expliqués dans le fichier d'[installation](https://github.com/Nicolik/MESCnn/blob/main/INSTALL.md). Cependant, si vous souhaitez exécuter le code sans GPU Nvidia, vous risquez d'avoir une erreur lors de l'exécution du code.
