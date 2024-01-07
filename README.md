# Project M1: Machine Learning Model Management

## Folders

* **Models/**: Contains models saved after execution of a notebook or the shell file.
* **Predictions/**: Stores CSV predictions generated after execution of a notebook or the shell file.
* **Classify/**: Should contain the data for model predictions. We used segmented glomeruli from the WSI provided by Dr. Gibier. Files are available [on the Nextcloud](https://nextcloud.dobial.com/s/YEFbFN3NyFnegiA) and on Teams.
* **DataClassification/**: Includes a `Dataset_glomeruli` subdirectory with data categorized (sclerosed or not) for creating splits, and a `Split_dataset` subdirectory with the split dataset (Train - Test - Validation). Files are available [n the Nextcloud](https://nextcloud.dobial.com/s/qd2QGrw7dZAJw7p) or on Teams.

## Automation

`Train_Model.sh` is a shell script for easy use. It creates data splits using a provided seed. If a seed is provided as an argument, it's passed to `Split_generator.py`. Without arguments, `Split_generator.py` runs with a random seed. Subsequently, `Model.py` runs for training a machine learning model.
Example:

- With a specific seed (444 here): `sh Train_Model.sh 444`
- With a random seed: `sh Train_Model.sh`

## Python Files

#### Split_generator.py

Splits the dataset into training, validation, and testing sets. Accepts an optional seed parameter for reproducibility.

#### Model.py

Contains the machine learning model (currently ViT-Base). It can be run using the shell script or manually by copying content from a desired notebook.

## Usage

There are two ways to use the notebooks/models:

1. Use `Train_Model.sh` to create splits and modify `Model.py`. (Recommended)
2. Manually run `Split_generator.py` to create splits, then use the notebooks.

To run a shell file on Linux: `sh Train_model.sh`

## Notebooks

#### CNN.ipynb

This notebook is designed for implementing and training a Convolutional Neural Network (CNN). It focuses on deep learning techniques, primarily using TensorFlow, to handle image processing tasks.

You can adjust various parameters in this notebook to fine-tune the model or modify the data processing. Some of the key parameters include:
\- batch_size: The size of the batch of images to be processed by the model. (Default is 20)
\- epochs: The number of epochs for training the model. (Default is 30)
\- learning_rate: The learning rate for the model's optimization algorithm. (Default is 0.001)
\- dropout_rate: The dropout rate for the neural network to prevent overfitting. (Default is 0.5)

##### Libraries

```
- TensorFlow: For building and training the CNN model.
- NumPy: For numerical operations.
- Matplotlib: For plotting and visualization.
- PIL (Python Imaging Library): For image manipulation.
- OS: For interacting with the operating system.
- CSV: For CSV file operations.
- SciPy: For scientific computing tasks.
```

#### google-vit-base-patch16-224.ipynb:

This notebook is designed for implementing and training a Convolutional Neural Network (CNN) using the Google Vision Transformer (ViT) base model with a 16x16 patch size and an input resolution of 224x224. It leverages deep learning techniques, focusing on the use of PyTorch and the transformers library.

You can adjust various parameters in this notebook to fine-tune the model or modify the data processing, including:

```
- num_epochs: The number of epochs for training the model. (Default is 30)
- batch_size: The size of the batch of images to be processed by the model. (Default is 30)
- learning_rate: The learning rate for the model's optimization algorithm. (Default is 0.0001)
- transform: A series of image transformations applied, including resizing to 224x224 (that you can't change since the model was pre-trained on that), and normalization with specified mean and standard deviation values.
```

##### Libraries

```
- PyTorch (torch): For building and training the CNN model.
- torchvision: For image processing and transformations.
- transformers: For implementing the Vision Transformer model.
- NumPy: For numerical operations.
- PIL (Python Imaging Library): For image manipulation.
- OS: For interacting with the operating system.
- CSV: For CSV file operations.
```

#### microsoft-resnet50.ipynb:

This notebook is designed for implementing and training a Convolutional Neural Network (CNN) using the Microsoft ResNet-50 model. It employs deep learning techniques with a focus on PyTorch.

You can adjust various parameters in this notebook to fine-tune the model or modify the data processing, including:

```
- num_epochs: The number of epochs for training the model. (Default is 30)
- batch_size: The size of the batch of images to be processed by the model. (Default is 30)
- learning_rate: The learning rate for the model's optimization algorithm. (Default is 0.0001)
- X: The number of layers in the ResNet-50 model to freeze during training.
- transform: A series of image transformations applied, including resizing to 256x256 (that you can't change since the model was pre-trained on that), and normalization with specified mean and standard deviation values.
```

##### Libraries

```
 - PyTorch (torch): For building and training the CNN model.
 - torchvision: For image processing and transformations.
 - transformers: For implementing advanced neural network models.
 - NumPy: For numerical operations.
 - PIL (Python Imaging Library): For image manipulation.
 - OS: For interacting with the operating system.
 - CSV: For CSV file operations.
```